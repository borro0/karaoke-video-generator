import QtQuick 2.0
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

Item {
    width: 580
    height: 400
    clip: true

    ScrollView {
        id: scrollView
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            bottom: parent.bottom
            leftMargin: 12
        }

        ColumnLayout {
            Item { Layout.preferredHeight: 4 } // padding
            spacing: 8
            anchors.fill: parent

            RowLayout {
                id: description

                Text {
                    text: "The project generator let's you setup a karaoke video project"
                }

                Image {
                    height: 200
                    width: 200
                    sourceSize.width: 200
                    sourceSize.height: 200
                    fillMode: Image.PreserveAspectCrop
                    source: "LRKB.jpg"
                }
            }

            RowLayout {

                Label {
                    text: "Title"
                    font.bold: true
                }

                TextField {
                    id: titleField
                    Layout.fillWidth: true
                    placeholderText: "Enter the title here ..."
                }
            }

            RowLayout {
                Label {
                    text: "Artist"
                    font.bold: true
                }
                TextField {
                    id: artistField
                    Layout.fillWidth: true
                    placeholderText: "Enter the artist here ..."
                }
            }

            RowLayout {
                Label {
                    text: "Bpm"
                    font.bold: true
                }

                TextField {
                    id: bpmField
                    inputMethodHints: Qt.ImhDigitsOnly
                    validator: IntValidator {bottom: 1; top: 300}
                    placeholderText: "Enter bpm here ..."
                }

                CheckBox {
                    id: shuffleCheckBox
                    text: "Shuffle?"
                    Layout.alignment: Qt.AlignBaseline
                    checked: false
                }
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "Activeer de SUPER MACHINE HACK COMPUTER!"
            }
        }
    }
}
