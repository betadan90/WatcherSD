module com.example.watcher_ui {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.watcher_ui to javafx.fxml;
    exports com.example.watcher_ui;
}