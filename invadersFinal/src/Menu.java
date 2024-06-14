import java.awt.*;

public class Menu {

    private static final Dimension WindowSize = new Dimension(800,600);
    private int highScore;




    public Menu(int highScore) {
        this.highScore = highScore;

    }

    public void paint(Graphics g){
        Font titleFont = new Font("Arial", Font.BOLD, 50);
        Font font1 = new Font("Arial", Font.PLAIN, 25);
        Font font2 = new Font("Arial", Font.PLAIN, 15);
        g.setFont(titleFont);
        g.setColor(Color.white);
        g.drawString("GAME OVER", 250, 100);
        g.setFont(font1);
      // g.drawString("High Score: " + invadersApp.updateHighScore(), 250, 300);
        g.drawString("Press spacebar to play", 250, 200);
        g.setFont(font2);
        g.drawString("[Arrow keys to move, spacebar to fire]", 250, 400);
       // g.drawString("High Score: " + highScore, 250, 300);

    }

}