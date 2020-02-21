import QtQuick 2.0
import QtQuick.Layouts 1.14

Item {
    width: 580
    height: 400
    clip: true

    Text {
        text: "hello from project generator!"
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Text {
                text: "The project generator let's you setup a karaoke video project"
            }
        }
    }
}
