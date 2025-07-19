import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
public class Command{
    Buttons playerButtons=new Buttons();
    Buttons player2Buttons=new Buttons();
    String type="buttons";
    private int playerCount=2;
    String saveGamePath="";
    JSONObject ObjectToJSON()
    {
        JSONObject json = new JSONObject();
        JSONObject p1ValuesJson=new JSONObject();
        p1ValuesJson.put("Up",playerButtons.up);
        p1ValuesJson.put("Down",playerButtons.down);
        p1ValuesJson.put("Left",playerButtons.left);
        p1ValuesJson.put("Right",playerButtons.right);
        p1ValuesJson.put("select",playerButtons.select);
        p1ValuesJson.put("start",playerButtons.start);
        p1ValuesJson.put("Y",playerButtons.buttonY);
        p1ValuesJson.put("B",playerButtons.buttonB);
        p1ValuesJson.put("X",playerButtons.buttonX);
        p1ValuesJson.put("A",playerButtons.buttonA);
        p1ValuesJson.put("L",playerButtons.buttonL);
        p1ValuesJson.put("R",playerButtons.buttonR);
        json.put("p1",p1ValuesJson);
        JSONObject p2ValuesJson=new JSONObject();
        p2ValuesJson.put("Up",player2Buttons.up);
        p2ValuesJson.put("Down",player2Buttons.down);
        p2ValuesJson.put("Left",player2Buttons.left);
        p2ValuesJson.put("Right",player2Buttons.right);
        p2ValuesJson.put("select",player2Buttons.select);
        p2ValuesJson.put("start",player2Buttons.start);
        p2ValuesJson.put("Y",player2Buttons.buttonY);
        p2ValuesJson.put("B",player2Buttons.buttonB);
        p2ValuesJson.put("X",player2Buttons.buttonX);
        p2ValuesJson.put("A",player2Buttons.buttonA);
        p2ValuesJson.put("L",player2Buttons.buttonL);
        p2ValuesJson.put("R",player2Buttons.buttonR);
        json.put("p2",p2ValuesJson);
        json.put("type",this.type);
        json.put("player_count",this.playerCount);
        json.put("savegamepath",this.saveGamePath);
        return json;
    }
}