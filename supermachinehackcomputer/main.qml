import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2

Item {
    visible: true
    width: 700
    height: 480

    TabView {
        anchors.fill: parent
        anchors.margins: 8
        Tab {
            id: projectGenerator
            title: "Project generator"
            ProjectGenerator { }
        }
        Tab {
            title: "Timing Tweaker"
            TimingTweaker {}
        }
    }


}
