import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
public class Player{
    int playerId;
    int health;
    int xCoord;
    int yCoord;
    int moveId;
    boolean isJumping;
    boolean isCrouching;
    boolean inMove;
    Buttons playerButtons;
    Player(JSONObject playerInfo)
    {
        this.playerId=playerInfo.getInt("character");
        this.health=playerInfo.getInt("health");
        this.xCoord=playerInfo.getInt("x");
        this.yCoord=playerInfo.getInt("y");
        this.moveId=playerInfo.getInt("move");
        this.isJumping=playerInfo.getBoolean("jumping");
        this.isCrouching=playerInfo.getBoolean("crouching");
        this.inMove=playerInfo.getBoolean("in_move");
        this.playerButtons=new Buttons(playerInfo.getJSONObject("buttons"));
    }
}