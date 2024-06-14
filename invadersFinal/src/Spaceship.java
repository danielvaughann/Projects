import java.awt.*;

public class Spaceship extends Sprite2D {
    private double xSpeed = 0;

    public Spaceship(Image i, Image j) {
        super(i, j); // invoke constructor on superclass Sprite2D
    }

    public void setXSpeed(double dx) {
        xSpeed = dx;
    }

    public void move() {

        x += xSpeed;

        //stop movement at screen edge
        if (x <= 0) {
            x = 0;
            xSpeed = 0;
        } else if (x >= winWidth - myImage.getWidth(null)) {
            x = winWidth - myImage.getWidth(null);
            xSpeed = 0;
        }
    }

    public double getY() {
        return y;
    }

    public double getX() {
        return x;
    }

    public boolean intersects(Alien alien) {
        if (alien != null && alien.myImage != null && myImage != null) { //checks if alien and ship intersects
            Rectangle shipBounds = new Rectangle((int) getX(), (int) getY(), myImage.getWidth(null), myImage.getHeight(null)); //rectangle represents a rectangle co ordinate space
            Rectangle alienBounds = new Rectangle((int) alien.getX(), (int) alien.getY(), alien.myImage.getWidth(null), alien.myImage.getHeight(null));
            return shipBounds.intersects(alienBounds);
        }
        return false;
    }
}

