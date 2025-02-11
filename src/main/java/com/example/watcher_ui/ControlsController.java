package com.example.watcher_ui;
import java.io.IOException;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.Scene;
import javafx.scene.Parent;
import javafx.stage.Stage;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.Button;
import javafx.util.Duration;

public class ControlsController {

    @FXML
    private Button previousButton;

    @FXML
    private Button manualButton;

    @FXML
    private Button autonomousButton;

    @FXML
    private Label timeLabel;

    @FXML
    private Label batteryLabel;

    @FXML
    private Label modeLabel;

    public void initialize() {

        Timeline timeline = new Timeline(
                new KeyFrame(Duration.seconds(1), event -> updateTime())
        );
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();
    }
    private void updateTime() {

        LocalTime currentTime = LocalTime.now();
        DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("hh:mm a");
        String timeString = currentTime.format(timeFormat);

        timeLabel.setText(timeString);
        timeLabel.setStyle("-fx-font-size: 15px; -fx-font-weight: bold;");
    }

    @FXML
    private void handlePreviousButton() throws IOException {

        FXMLLoader loader = new FXMLLoader(getClass().getResource("Home.fxml"));
        Parent homeRoot = loader.load();

        Stage stage = (Stage) previousButton.getScene().getWindow();
        Scene homeScene = new Scene(homeRoot);
        stage.setScene(homeScene);
    }

    @FXML
    private void handleManualButton() {
        modeLabel.setText("Manual");
    }

    @FXML
    private void handleAutoButton() {
        modeLabel.setText("Autonomous");
    }

    public void dynamicLabels(String time, String battery) {

        timeLabel.setText(time);
        batteryLabel.setText(battery);
    }
}


