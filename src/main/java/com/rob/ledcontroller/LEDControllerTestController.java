package com.rob.ledcontroller;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.ColorPicker;
import javafx.scene.layout.Background;
import javafx.scene.layout.Region;

import java.net.URL;
import java.util.ResourceBundle;

/**
 * Created by Robin on 10/30/2015.
 */
public class LEDControllerTestController implements Initializable{

    @FXML
    Region mainRegion;
    @FXML
    ColorPicker colorPicker;


    @Override
    public void initialize(URL location, ResourceBundle resources) {
        System.out.println("Main region : " + mainRegion);
        System.out.println("Color Picker : " + colorPicker);
    }
}
