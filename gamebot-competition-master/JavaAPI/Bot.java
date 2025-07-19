
public class Bot{

    Command fight(GameState gameState, String player){
        //the function you have to implement
        Command myCommand=new Command();
        if (player.equals("1")){
             myCommand.playerButtons.up=true; //Example of changing the values (Jumping)   
            }
        else if (player.equals("2")){
            myCommand.player2Buttons.up=true;
        }
        /*
                    YOUR CODE GOES HERE
        You need to change the values of the playerButtons if your player is player1 and if your player
        is player2 then change player2Buttons respectively.
        
        */
        return myCommand;
    }

}