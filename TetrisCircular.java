// TetrisCircular.java — круговой тетрис на Java (Swing)

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class TetrisCircular extends JPanel implements ActionListener, KeyListener {
    // Аналогичная реализация (полный код можно дополнить)
    public static void main(String[] args) {
        JFrame frame = new JFrame("🌀 TetrisCircular");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 600);
        frame.setVisible(true);
    }
    @Override public void actionPerformed(ActionEvent e) {}
    @Override public void keyPressed(KeyEvent e) {}
    @Override public void keyReleased(KeyEvent e) {}
    @Override public void keyTyped(KeyEvent e) {}
}
