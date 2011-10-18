// NoTippingApplet
//
// version 1.0
// location: \java\notipping\
//
// Tyler Neylon, 2002
//

import java.applet.*;
import java.lang.*;
import java.awt.*;
import java.awt.event.*;

public class NoTippingApplet
        extends Applet {

    public void init() {
    }

	public void start() {
		new NoTippingFrame();
	}

    public static void main(String[] args) {
        final Applet applet = new NoTippingApplet();
        System.runFinalizersOnExit(true);
        Frame frame = new Frame ("MyApplet");
        frame.addWindowListener (new WindowAdapter() {
            public void windowClosing (WindowEvent event) {
                applet.stop();
                applet.destroy();
                System.exit(0);
            }
        });
        frame.add ("Center", applet);
        NoTippingAppletStub noTippingAppletStub = new NoTippingAppletStub(args, applet);
        Player.setProperties(noTippingAppletStub);
        applet.setStub (noTippingAppletStub);
        frame.show();
        applet.init();
        applet.start();
        frame.pack();
    }
}

class NoTippingFrame extends Frame {
	public NoTippingFrame() {
		setLayout(new BorderLayout());
		NoTippingComponent main_display = new NoTippingComponent();
		add(main_display, "Center");
		Container toolbar = new Panel();
		GridBagLayout gbl = new GridBagLayout();
		GridBagConstraints gbc = new GridBagConstraints();
		toolbar.setLayout(gbl);
		gbc.fill = GridBagConstraints.BOTH;
		gbc.weightx = 1.0;

        addChoice("red", Player.getPlayers(), main_display, gbl, gbc, toolbar);
        addChoice("blue", Player.getPlayers(), main_display, gbl, gbc, toolbar);

        addButton("Connect", main_display, gbl, gbc, toolbar);
        addButton("Restart", main_display, gbl, gbc, toolbar);

        addButton("Undo", main_display, gbl, gbc, toolbar);

		/*
		b = new Button("Forward");
		b.setActionCommand("Forward");
		b.addActionListener(main_display);
		gbl.setConstraints(b, gbc);
		toolbar.add(b);
		*/

		TextField tf = new TextField();
		//tf.setActionCommand("Hi");
		tf.addActionListener(main_display);
		gbl.setConstraints(tf, gbc);
		toolbar.add(tf);

        addButton("Help", main_display, gbl, gbc, toolbar);

		/*
		b = new Button("Options");
		gbl.setConstraints(b, gbc);
		toolbar.add(b);
		*/

		addWindowListener(new WindowCloser());

		add(toolbar, "North");
		setTitle("The No Tipping Game");
		pack();
		setVisible(true);
		setEnabled(true);
	}

    private void addButton(String name, NoTippingComponent main_display, GridBagLayout gbl, GridBagConstraints gbc, Container toolbar) {
        Button b = new Button(name);
        b.setActionCommand(name);
        b.addActionListener(main_display);
        gbl.setConstraints(b, gbc);
        toolbar.add(b);
    }

    private void addChoice(String name, String[] choices, NoTippingComponent main_display, GridBagLayout gbl, GridBagConstraints gbc, Container toolbar) {
        Choice c = new Choice();
        for (int i=0; i<choices.length; i++)
            c.addItem(choices[i]);
        c.setName(name);
        c.addItemListener(main_display);
        gbl.setConstraints(c, gbc);
        toolbar.add(c);
    }
}

class WindowCloser extends WindowAdapter {
	public void windowClosing(WindowEvent e) {
		System.out.println("windowClosing(WindowEvent)");
		e.getWindow().dispose();
	}
}

