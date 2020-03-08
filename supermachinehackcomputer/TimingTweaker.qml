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
            width: 550

            Item { Layout.preferredHeight: 4 } // padding
            spacing: 8
            anchors.fill: parent

            RowLayout {
                id: description

                TextArea {
                    width: 300
                    text: "The timing tweaker let's alter the timing of the whole text track"
                    wrapMode: TextEdit.WrapAnywhere
                    readOnly: true
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
                width: parent.fill

                Label {
                    text: "Delay"
                    font.bold: true
                }

                TextField {
                    id: delayField
                    Layout.preferredWidth: 400
                    inputMethodHints: Qt.ImhFormattedNumbersOnly
                    validator: IntValidator {bottom: -300; top: 300}
                    placeholderText: "Enter time to delay (in seconds, can be negative!)"
                }
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                text: "Activeer de SUPER MACHINE HACK COMPUTER TIMING TWEAKER!"
                background: Rectangle {
                    color: "gold"
                }
            }
        }
    }
}
