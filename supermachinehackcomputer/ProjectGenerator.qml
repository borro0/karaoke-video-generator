import QtQuick 2.0
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import CustomTypes 1.0

Item {
    clip: true

    PythonCaller {
        id: pythonCaller
        program: "project_generator.py"
    }

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

            RowLayout {
                id: description

                TextArea {
                    width: 300
                    text: "The project generator let's you setup a karaoke video project"
                    wrapMode: TextEdit.WrapAnywhere
                    readOnly: true
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
                    enabled: !customCheckBox.checked
                }

                CheckBox {
                    id: shuffleCheckBox
                    text: "Shuffle?"
                    Layout.alignment: Qt.AlignBaseline
                    checked: false
                    enabled: !customCheckBox.checked
                }

                CheckBox {
                    id: customCheckBox
                    text: "Custom"
                    Layout.alignment: Qt.AlignBaseline
                    checked: false
                }
            }

            CheckBox {
                id: forceCheckBox
                text: "Do you allow to overwrite an existing project?"
                Layout.alignment: Qt.AlignBaseline
                checked: false
            }

            Button {
                Layout.alignment: Qt.AlignHCenter                
                text: "Activeer de SUPER MACHINE HACK COMPUTER PROJECT GENERATOR!"
                background: Rectangle {
                    color: "gold"
                }
                onPressed: pythonCaller.run(titleField.text, artistField.text, bpmField.text, shuffleCheckBox.checked, forceCheckBox.checked)
            }

            Image {
                sourceSize.width: 200
                sourceSize.height: 150
                fillMode: Image.PreserveAspectCrop
                source: "images/computer.jfif"
            }
        }
    }
}
