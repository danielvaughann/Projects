import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.image.*;

public class InvadersApplication extends JFrame implements Runnable, KeyListener {

    // member data
    private static String workingDirectory;
    private static boolean isInitialised = false;
    private static final Dimension WindowSize = new Dimension(800, 600);
    private BufferStrategy strategy;
    private Graphics offscreenGraphics;
    private static final int NUMALIENS = 30;
    private Alien[] AliensArray = new Alien[NUMALIENS];
    public Spaceship PlayerShip;
    public Image bulletImage;
    public PlayerBullet bullet;
    Image alienImage;
    Image alienImage2;
    private PlayerBullet[] bullets; // Array to hold multiple bullets
    private static final int MAX_BULLETS = 20;
    //maximum number of bullets allowed
    private boolean[] alienAlive = new boolean[NUMALIENS];
    boolean playing;


    private int score = 0;
    private int highScore = 0;

    private enum STATE { //allows me to change between title and menu
        MENU,
        GAME
    }

    ;

    private STATE State = STATE.MENU; //starts of in game
    private Menu menu;


    // constructor
    public InvadersApplication() {
        //Display the window, centred on the screen
        Dimension screensize = java.awt.Toolkit.getDefaultToolkit().getScreenSize();
        int x = screensize.width / 2 - WindowSize.width / 2;
        int y = screensize.height / 2 - WindowSize.height / 2;
        setBounds(x, y, WindowSize.width, WindowSize.height);
        setVisible(true);
        this.setTitle("Space Invaders! .. (getting there)");


        // load image from disk
        ImageIcon icon = new ImageIcon(workingDirectory + "/alien_ship_1.png");
        Image alienImage = icon.getImage();
        ImageIcon icon2 = new ImageIcon(workingDirectory + "/alien_ship_2.png");
        Image alienImage2 = icon2.getImage();
        ImageIcon iconBullet = new ImageIcon(workingDirectory + "/bullet.png");
        bulletImage = iconBullet.getImage();
        bullets = new PlayerBullet[MAX_BULLETS]; // Initialize the bullets array


        // create and initialise some aliens, passing them each the image we have loaded
        for (int i = 0; i < NUMALIENS; i++) {
            AliensArray[i] = new Alien(alienImage, alienImage2);

            double xx = (i % 5) * 80 + 70;
            double yy = (i / 5) * 40 + 50; // integer division!
            AliensArray[i].setPosition(xx, yy);
        }
        Alien.setFleetXSpeed(Alien.getFleetXSpeed() * 2); // Increase the speed by 20%


        // create and initialise the player's spaceship
        icon = new ImageIcon(workingDirectory + "/player_ship.png");
        Image shipImage = icon.getImage();
        PlayerShip = new Spaceship(shipImage, shipImage);
        PlayerShip.setPosition(300, 530);
        menu = new Menu(highScore);

        // tell all sprites the window width
        Sprite2D.setWinWidth(WindowSize.width);
State= STATE.GAME;

        // create and start our animation thread
        Thread t = new Thread(this);
        t.start();

        // send keyboard events arriving into this JFrame back to its own event handlers
        addKeyListener(this);

        // initialise double-buffering
        createBufferStrategy(2);
        strategy = getBufferStrategy();
        offscreenGraphics = strategy.getDrawGraphics();

        isInitialised = true;
    }

    // thread's entry point
    public void run() {
        while (1 == 1) {

            // 1: sleep for 1/50 sec
            try {
                Thread.sleep(20);
            } catch (InterruptedException e) {
            }

            // 2: animate game objects
            boolean alienDirectionReversalNeeded = false;
            for (int i = 0; i < NUMALIENS; i++) {
                if (AliensArray[i].move() && !alienAlive[i])
                    alienDirectionReversalNeeded = true;
            }
            if (alienDirectionReversalNeeded) {
                Alien.reverseDirection();
                for (int i = 0; i < NUMALIENS; i++)
                    AliensArray[i].jumpDownwards();
            }
            for (int i = 0; i < NUMALIENS; i++) {
                if (alienAlive[i] && AliensArray[i] != null && PlayerShip.intersects(AliensArray[i])) {
                    State = STATE.MENU;  //game over switch to menu state
                }
            }
            if (score > highScore) {
                highScore = score; //updates highscore in real time
            }

            for (int i = 0; i < bullets.length; i++) {
                if (bullets[i] != null) {
                    bullets[i].moveBullet(); //moves 10 pixels
                    if (bullets[i].getY() < 0) {
                        bullets[i] = null; //remove bullet if it goes off-screen
                    }
                }
            }
            checkCollisions(); //checks for bullets and alien collisons

            PlayerShip.move(); //moves playership left to right

            // 3: force an application repaint
            this.repaint();
        }
    }


    private int setAlienSpeed = 2;
    public void startNewWave() {

        for (int i = 0; i < NUMALIENS; i++) {
            alienAlive[i] = false; //resets all aliens to alive
        }
        for (int i = 0; i < NUMALIENS; i++) {
            double xx = (i % 5) * 80 + 70;
            double yy = (i / 5) * 40 + 50;
            AliensArray[i].setPosition(xx, yy);
        }
        setAlienSpeed *= 2;
        Alien.setFleetXSpeed(setAlienSpeed); //increase the speed by 20%

        //reset the alienAlive array
        for (int f = 0; f < NUMALIENS; f++) {
            alienAlive[f] = false;
        }
    }



    public void startNewGame() {
        //reset the score and game state
        if (score > highScore) {
            highScore = score;
        }
score =0;



        //reset player's ship position
        PlayerShip.setPosition(300, 530);


        setAlienSpeed = 1; //reset the alien speed to its initial value
        Alien.setFleetXSpeed(setAlienSpeed);

        for (int i = 0; i < NUMALIENS; i++) {
            double xx = (i % 5) * 80 + 70;
            double yy = (i / 5) * 40 + 50;
            AliensArray[i].setPosition(xx, yy);
            alienAlive[i] = false;
        }


        State = STATE.GAME;
    }

    // Three Keyboard Event-Handler functions
    public void keyPressed(KeyEvent e) {
        if (State == STATE.MENU && e.getKeyCode() == KeyEvent.VK_SPACE) {
            //transition to gameplay state when SPACE is pressed on the title screen
            State = STATE.GAME ;


        } else if (State == STATE.GAME  && e.getKeyCode() == KeyEvent.VK_ESCAPE) {
            //transition back to title state when ESC is pressed during gameplay
            State = STATE.MENU;

        }

        if (e.getKeyCode() == KeyEvent.VK_LEFT)
            PlayerShip.setXSpeed(-4);
        else if (e.getKeyCode() == KeyEvent.VK_RIGHT)
            PlayerShip.setXSpeed(4);
        else if (e.getKeyCode() == KeyEvent.VK_SPACE)
            for (int i = 0; i < bullets.length; i++) {
                if (bullets[i] == null) {
                    bullets[i] = new PlayerBullet(bulletImage, alienImage, alienImage2, PlayerShip.getX(), PlayerShip.getY());
                    break; //exit loop once a bullet is added
                }
            }
    }


    public void keyReleased(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_LEFT || e.getKeyCode() == KeyEvent.VK_RIGHT)
            PlayerShip.setXSpeed(0);
    }

    public void keyTyped(KeyEvent e) {
    }
    //

    // application's paint method
    public void paint(Graphics g) {
        if (!isInitialised)
            return;

        g = offscreenGraphics;

        //clear the canvas with a big black rectangle
        g.setColor(Color.BLACK);
        g.fillRect(0, 0, WindowSize.width, WindowSize.height);

        if (State == STATE.GAME) {
            //redraws all game objects
            for (int i = 0; i < NUMALIENS; i++)
                if (!alienAlive[i]) {
                    AliensArray[i].paint(g);
                }
            PlayerShip.paint(g);
            for (int i = 0; i < bullets.length; i++) {
                if (bullets[i] != null) {
                    bullets[i].paint(g);
                }
            }
            g.setColor(Color.WHITE);
            g.setFont(new Font("Arial", Font.PLAIN, 16));
            g.drawString("Score: " + score, WindowSize.width - 100, 50);
            g.drawString("High Score: " + highScore, WindowSize.width - 130, 100);
        }
        if (State == STATE.MENU) {
            menu.paint(g);
        }
        // flip the buffers offscreen<-->onscreen
        strategy.show();
    }



    public void checkCollisions() {
        //iterate through all bullets
        for (int i = 0; i < bullets.length; i++) {
            PlayerBullet bullet = bullets[i];
            if (bullet != null) {
                //iterate through all aliens
                for (int j = 0; j < AliensArray.length; j++) {
                    if (!alienAlive[j]) {
                        Alien alien = AliensArray[j];
                        if (alien != null) {
                            //check for collision between the bullet and the alien
                            if (bullet.getX() >= alien.getX() && bullet.getX() <= alien.getX() + alien.myImage.getWidth(null) &&
                                    bullet.getY() >= alien.getY() && bullet.getY() <= alien.getY() + alien.myImage.getHeight(null)) {
                                // Remove the bullet and the alien if a collision is detected
                                alienAlive[j] = true;
                                bullets[i] = null;
                                score+=10;
                                break; //exit the inner loop once a collision is detected
                            }
                        }
                    }
                }
            }
        }
        if (areAllAliensDead()) {
            startNewWave(); //start a new wave if all aliens are dead
        }
        for (int i = 0; i < AliensArray.length; i++) {
           // if (!alienAlive[i]) {
                Alien alien = AliensArray[i];
                if (alien != null && !alienAlive[i] && PlayerShip.intersects(alien)) {
                    //game over switch to menu state
                    if (score > highScore) {
                        highScore = score;
                        updateHighScore();
                    }
                    startNewGame(); //resets game
                    State=STATE.MENU;
                    break;
                }
            }
        //}
    }
    public boolean areAllAliensDead() {
        for (int i = 0; i < NUMALIENS; i++) {
            if (!alienAlive[i]) {
                return false; //if any alien is alive return false
            }
        }
        return true; //if all aliens are dead return true
    }
    public int updateHighScore() {
        if (score > highScore) {
            highScore = score;
            return highScore;
        }
        return score;
    }


    public static void main(String[] args) {
        workingDirectory = System.getProperty("user.dir");
        System.out.println("Working Directory = " + workingDirectory);
        InvadersApplication w = new InvadersApplication();
    }

}