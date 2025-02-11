package com.example.watcher_ui;
import java.io.IOException;
import javafx.fxml.FXMLLoader;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.Parent;

public class Main extends Application {

    @Override

    public void start(Stage stage) throws IOException {

        FXMLLoader fxmlloader = new FXMLLoader(getClass().getResource("Home.fxml"));
        Scene scene = new Scene(fxmlloader.load());
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {

        launch();
    }
}