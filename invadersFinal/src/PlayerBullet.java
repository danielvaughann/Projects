import java.awt.*;

public class PlayerBullet extends Sprite2D{

    private int bulletSpeed = 10;
    Image bulletImage;

    public PlayerBullet(Image image,Image i1,Image i2,double x,double y){
        super(i1,i2);
        setPosition(x,y);
        this.bulletImage = image;

    }
    public void moveBullet(){
        y-=bulletSpeed;

    }

    public double getY(){
        return y;
    }
    public double getX(){
        return x;
    }
    @Override
    public void paint(Graphics g){
        g.drawImage(bulletImage,(int)x+25,(int)y+25,null);
    }



}