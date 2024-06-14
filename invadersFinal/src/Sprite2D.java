import java.awt.*;

public class Sprite2D {
    int framesDrawn=0;
    // member data
    protected double x,y;
    protected Image myImage;
    protected Image myImage2;

    // static member data
    protected static int winWidth;

    // constructor
    public Sprite2D(Image i, Image j) {
        myImage = i;
        myImage2 = j;
    }

    public void setPosition(double xx, double yy) {
        x=xx;
        y=yy;
    }


    public void paint(Graphics g) {
        framesDrawn++;
        if ( framesDrawn%100<50 ) //changes alien image
            g.drawImage(myImage, (int)x, (int)y, null);
        else
            g.drawImage(myImage2, (int)x, (int)y, null);
    }


    public static void setWinWidth(int w) {
        winWidth = w;
    }
}
