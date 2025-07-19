import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
public class Buttons{
    public boolean up;
    boolean down;
    boolean right;
    boolean left;
    boolean select;
    boolean start;
    boolean buttonY;
    boolean buttonB;
    boolean buttonX;
    boolean buttonA;
    boolean buttonL;
    boolean buttonR;
    Buttons()
    {
        this.up=false;
        this.down=false;
        this.right=false;
        this.left=false;
        this.select=false;
        this.start=false;
        this.buttonY=false;
        this.buttonB=false;
        this.buttonX=false;
        this.buttonA=false;
        this.buttonL=false;
        this.buttonR=false;
    }
    Buttons(JSONObject buttons)
    {
        this.up=buttons.getBoolean("Up");
        this.down=buttons.getBoolean("Down");
        this.right=buttons.getBoolean("Right");
        this.left=buttons.getBoolean("Left");
        this.select=buttons.getBoolean("Select");
        this.start=buttons.getBoolean("Start");
        this.buttonY=buttons.getBoolean("Y");
        this.buttonB=buttons.getBoolean("B");
        this.buttonX=buttons.getBoolean("X");
        this.buttonA=buttons.getBoolean("A");
        this.buttonL=buttons.getBoolean("L");
        this.buttonR=buttons.getBoolean("R");    
    }
}