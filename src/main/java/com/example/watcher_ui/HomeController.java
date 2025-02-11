package com.example.watcher_ui;
import java.io.IOException;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.Scene;
import javafx.scene.Parent;
import javafx.stage.Stage;
import javafx.fxml.FXMLLoader;
import javafx.scene.control.Button;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.util.Duration;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import javafx.scene.text.Font;

public class HomeController {

    @FXML
    private Button controlsButton;

    @FXML
    private Button navButton;

    @FXML
    private Button settingsButton;

    @FXML
    private Label timeLabel;

    @FXML
    private Label dateLabel;

    public void initialize() {

        Timeline timeline = new Timeline(
                new KeyFrame(Duration.seconds(1), event -> updateTime())
        );
        timeline.setCycleCount(Timeline.INDEFINITE);
        timeline.play();

        LocalDate todaysDate = LocalDate.now();

        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("EEEE, MMMM d, yyyy");
        dateLabel.setStyle("-fx-font-weight: bold;");
        dateLabel.setFont(Font.font(dateLabel.getFont().getFamily(), 15));

        String formattedDate = todaysDate.format(dateFormat);
        dateLabel.setText(formattedDate);
    }
    private void updateTime() {

        LocalTime currentTime = LocalTime.now();
        DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("hh:mm a");
        String timeString = currentTime.format(timeFormat);

        timeLabel.setText(timeString);
        timeLabel.setStyle("-fx-font-size: 30px; -fx-font-weight: bold;");
    }

    @FXML
    private Label batteryLabel;
    @FXML
    private Label weatherLabel;

    @FXML
    private void goToControlsButton() throws IOException {

        FXMLLoader loader = new FXMLLoader(getClass().getResource("Controls.fxml"));
        Parent controlsRoot = loader.load();

        Stage stage = (Stage) controlsButton.getScene().getWindow();
        Scene controlsScene = new Scene(controlsRoot);
        stage.setScene(controlsScene);
    }

    public void dynamicLabels(String time, String battery, String weather) {

        timeLabel.setText(time);
        batteryLabel.setText(battery);
        weatherLabel.setText(weather);
    }

}