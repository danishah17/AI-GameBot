import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
public class GameState{
    Player player1;
    Player player2;
    int timer;
    String fightResult;
    boolean hasRoundStarted;
    boolean isRoundOver;
    GameState(JSONObject allInfo)
    {
        this.player1=new Player(allInfo.getJSONObject("p1"));
        this.player2=new Player(allInfo.getJSONObject("p2"));
        this.timer=allInfo.getInt("timer");
        this.fightResult=allInfo.getString("result");
        this.hasRoundStarted=allInfo.getBoolean("round_started");
        this.isRoundOver=allInfo.getBoolean("round_over");
    }
}