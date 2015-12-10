package com.rob.ws2801driver;

import java.util.Random;

import com.pi4j.wiringpi.Gpio;
import com.pi4j.wiringpi.Spi;

/**
 * Created by Robin on 11/12/2015.
 */
public class WS2801Driver {


    public static void main(String[] args) {

        System.out.println("Test 2!");

        System.out.println("Out:" + Spi.wiringPiSPISetup(0, 500000));// 1mhz=1000000
        System.out.println("Out:" + Gpio.wiringPiSetupSys());
        int num_leds = 110;
        try {
            // Using a file vs wiringPi:
            //
            // FileOutputStream fos = new FileOutputStream(new
            // File("/dev/spidev0.0"));
            // fos.write(colors);
            // fos.flush(); //limited success with this

            Random randomGenerator = new Random();
            for (; ; ) {
                int colorToUse1 = randomGenerator.nextInt(255);
                int colorToUse2 = randomGenerator.nextInt(255);
                int colorToUse3 = randomGenerator.nextInt(255);
                long startTimeMillis = System.currentTimeMillis();

                // fade all lights out...

                for (int j = 0; j < 255; j++) {
                    byte[] colors = new byte[num_leds * 3];
                    for (int i = 0; i < num_leds * 3; i = i + 3) {
                        colors[i] = (byte) colorToUse1;
                        colors[i + 1] = (byte) colorToUse2;
                        colors[i + 2] = (byte) colorToUse3;
                    }
                    if (colorToUse1 != 0)
                        colorToUse1--;
                    if (colorToUse2 != 0)
                        colorToUse2--;
                    if (colorToUse3 != 0)
                        colorToUse3--;
                    Spi.wiringPiSPIDataRW(1, colors, colors.length);
                    Gpio.delayMicroseconds(800); // need to determine optimal value
                }
                System.out.println("Elapsed:"
                        + (System.currentTimeMillis() - startTimeMillis));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
