import java.awt.Image;

public class Alien extends Sprite2D {
    private static double xSpeed=1;

    public Alien(Image i, Image j) {
        super(i,j);
    }

    public static double getFleetXSpeed() {
        return xSpeed;
    }

    public boolean move() {
        x+=xSpeed;


        if (x<=0 || x>=winWidth-myImage.getWidth(null)) //keeps playership within boundarys
            return true;
        else
            return false;
    }

    public static void setFleetXSpeed(double dx) {
        xSpeed=dx;
    }

    public static void reverseDirection() {

        xSpeed=-xSpeed; //changes direction when a wall is hit
        if(xSpeed>0){
            xSpeed+=2;
        }else {
            xSpeed-=2;
        }
    }

    public void jumpDownwards() {
        y+=20;
    }
    public double getY(){
        return y;
    }
    public double getX(){
        return x;
    }
}

