import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Super Machine Hack Computer")

    TabView {
        anchors.fill: parent
        anchors.margins: 8
        Tab {
            id: projectGenerator
            title: "Project generator"
            FileDialogs { }
        }
        Tab {
            id:
            title: "Color"
            ColorDialogs { }
        }
        Tab {
            title: "Font"
            FontDialogs { anchors.fill: parent }
        }
        Tab {
            title: "Message"
            MessageDialogs { anchors.fill:parent }
        }
        Tab {
            title: "Custom"
            CustomDialogs { anchors.fill:parent }
        }
    }


}
