import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import csv
import time
from command import Command
from buttons import Buttons
from game_state import GameState
from player import Player

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )
    
    def forward(self, x):
        return self.network(x)

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
        return np.array(state), action, reward, np.array(next_state), done
    
    def __len__(self):
        return len(self.buffer)

class Bot:
    def __init__(self):
        self.actions = [
            ["<", "<", "!<"],  # Move left
            [">", ">", "!>"],  # Move right
            ["v+R", "v+R", "!v+!R"],  # Attack
            ["<", "-", "!<", "v+<", "-", "!v+!<", "v", "-", "!v", "v+>", "-", "!v+!>", ">+Y", "-", "!>+!Y"],  # Fire
            ["<+^+B", "<+^+B", "!<+!^+!B"]  # Spin
        ]
        self.action_size = len(self.actions)
        self.state_size = 8
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(self.state_size, self.action_size).to(self.device)
        self.target_model = DQN(self.state_size, self.action_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.memory = ReplayBuffer(10000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.my_command = Command()
        self.buttn = Buttons()
        self.exe_code = 0
        self.remaining_code = []
        self.prev_health = {'1': None, '2': None}
        self.prev_state = None
        self.prev_action = None
        self.characters = [f"char_{i}" for i in range(10)]  # Placeholder for 10 characters
        self.current_character = None
        self.round_id = 0
        self.csv_file = "game_dataset.csv"
        self.csv_initialized = False

    def get_state(self, current_game_state, player):
        if player == "1":
            diff = current_game_state.player2.x_coord - current_game_state.player1.x_coord
            player_health = current_game_state.player1.health
            opponent_health = current_game_state.player2.health
            player_buttons = current_game_state.player1.player_buttons
            opponent_buttons = current_game_state.player2.player_buttons
        else:
            diff = current_game_state.player1.x_coord - current_game_state.player2.x_coord
            player_health = current_game_state.player2.health
            opponent_health = current_game_state.player1.health
            player_buttons = current_game_state.player2.player_buttons
            opponent_buttons = current_game_state.player1.player_buttons
        
        player_attacking = 1.0 if getattr(player_buttons, 'Y', False) or getattr(player_buttons, 'B', False) else 0.0
        opponent_attacking = 1.0 if getattr(opponent_buttons, 'Y', False) or getattr(opponent_buttons, 'B', False) else 0.0
        
        state = np.array([
            diff / 100.0,
            player_health / 100.0,
            opponent_health / 100.0,
            current_game_state.timer / 100.0,
            player_attacking,
            opponent_attacking,
            1.0 if current_game_state.has_round_started else 0.0,
            1.0 if current_game_state.is_round_over else 0.0
        ])
        return state

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state)
        return q_values.argmax().item()

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        
        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_model(next_states).max(1)[0]
        target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
        
        loss = nn.MSELoss()(q_values, target_q_values.detach())
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(0.01 * param.data + 0.99 * target_param.data)

    def log_to_csv(self, round_id, state, action_idx):
        timestamp = time.time()
        row = [
            round_id,
            timestamp,
            state[0],  # diff
            state[1],  # player_health
            state[2],  # opponent_health
            state[3],  # timer
            state[4],  # player_attacking
            state[5],  # opponent_attacking
            state[6],  # has_round_started
            state[7],  # is_round_over
            action_idx,
            self.current_character
        ]
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not self.csv_initialized:
                writer.writerow([
                    'round_id', 'timestamp', 'diff', 'player_health', 'opponent_health',
                    'timer', 'player_attacking', 'opponent_attacking', 'has_round_started',
                    'is_round_over', 'action_idx', 'character_id'
                ])
                self.csv_initialized = True
            writer.writerow(row)

    def fight(self, current_game_state, player):
        if current_game_state.is_round_over:
            self.exe_code = 0
            self.remaining_code = []
            self.prev_health[player] = None
            self.prev_state = None
            self.my_command = Command()
            self.round_id += 1
            self.current_character = random.choice(self.characters)  # Random character for next round
            return self.my_command

        if not current_game_state.has_round_started:
            return self.my_command

        if self.prev_health[player] is None:
            self.prev_health[player] = current_game_state.player1.health
            self.prev_health['2' if player == "1" else '1'] = current_game_state.player2.health
            self.current_character = random.choice(self.characters)  # Initial character

        if self.exe_code != 0:
            self.run_command([], current_game_state.player1 if player == "1" else current_game_state.player2)
        else:
            state = self.get_state(current_game_state, player)
            action_idx = self.select_action(state)
            command = self.actions[action_idx]
            self.run_command(command, current_game_state.player1 if player == "1" else current_game_state.player2)
            
            # Log to CSV
            self.log_to_csv(self.round_id, state, action_idx)

        if player == "1":
            self.my_command.player_buttons = self.buttn
        else:
            self.my_command.player2_buttons = self.buttn

        current_health = current_game_state.player1.health if player == "1" else current_game_state.player2.health
        opponent_health = current_game_state.player2.health if player == "1" else current_game_state.player1.health
        prev_opponent_health = self.prev_health['2' if player == "1" else '1']
        
        reward = -0.1
        if current_health < self.prev_health[player]:
            reward -= 10
        if prev_opponent_health is not None and opponent_health < prev_opponent_health:
            reward += 10
        if current_game_state.is_round_over:
            if current_health > opponent_health:
                reward += 100
            elif current_health < opponent_health:
                reward -= 100

        next_state = self.get_state(current_game_state, player)
        done = current_game_state.is_round_over
        if self.prev_state is not None:
            self.memory.push(self.prev_state, self.prev_action, reward, next_state, done)
            self.train()
        
        self.prev_state = state
        self.prev_action = action_idx
        self.prev_health[player] = current_health
        self.prev_health['2' if player == "1" else '1'] = opponent_health
        
        return self.my_command

    def run_command(self, com, player):
        if self.exe_code - 1 == len(self.fire_code):
            self.exe_code = 0
            self.remaining_code = []
            print("complete")
        elif len(self.remaining_code) == 0:
            self.fire_code = com
            self.exe_code += 1
            self.remaining_code = self.fire_code[0:]
        else:
            self.exe_code += 1
            if self.remaining_code[0] == "v+<":
                self.buttn.down = True
                self.buttn.left = True
                print("v+<")
            elif self.remaining_code[0] == "!v+!<":
                self.buttn.down = False
                self.buttn.left = False
                print("!v+!<")
            elif self.remaining_code[0] == "v+>":
                self.buttn.down = True
                self.buttn.right = True
                print("v+>")
            elif self.remaining_code[0] == "!v+!>":
                self.buttn.down = False
                self.buttn.right = False
                print("!v+!>")
            elif self.remaining_code[0] == ">+Y":
                self.buttn.Y = True
                self.buttn.right = True
                print(">+Y")
            elif self.remaining_code[0] == "!>+!Y":
                self.buttn.Y = False
                self.buttn.right = False
                print("!>+!Y")
            elif self.remaining_code[0] == "<+Y":
                self.buttn.Y = True
                self.buttn.left = True
                print("<+Y")
            elif self.remaining_code[0] == "!<+!Y":
                self.buttn.Y = False
                self.buttn.left = False
                print("!<+!Y")
            elif self.remaining_code[0] == ">+^+B":
                self.buttn.right = True
                self.buttn.up = True
                self.buttn.B = not player.player_buttons.B
                print(">+^+B")
            elif self.remaining_code[0] == "!>+!^+!B":
                self.buttn.right = False
                self.buttn.up = False
                self.buttn.B = False
                print("!>+!^+!B")
            elif self.remaining_code[0] == "v+R":
                self.buttn.down = True
                self.buttn.R = not player.player_buttons.R
                print("v+R")
            elif self.remaining_code[0] == "!v+!R":
                self.buttn.down = False
                self.buttn.R = False
                print("!v+!R")
            else:
                if self.remaining_code[0] == "v":
                    self.buttn.down = True
                    print("down")
                elif self.remaining_code[0] == "!v":
                    self.buttn.down = False
                    print("Not down")
                elif self.remaining_code[0] == "<":
                    self.buttn.left = True
                    print("left")
                elif self.remaining_code[0] == "!<":
                    self.buttn.left = False
                    print("Not left")
                elif self.remaining_code[0] == ">":
                    self.buttn.right = True
                    print("right")
                elif self.remaining_code[0] == "!>":
                    self.buttn.right = False
                    print("Not right")
            self.remaining_code = self.remaining_code[1:]
        return