
import QtQuick 2.12
import QtQuick.Controls 2.12
//import PortfoliosModel

Page {
    width: 640
    height: 480
    required property var myModel

    header: Label {
        color: "#15af15"
        text: qsTr("Where do people use Qt?")
        font.pointSize: 17
        font.bold: true
        font.family: "Arial"
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        padding: 10
    }
    Rectangle {
        id: root
        width: parent.width
        height: parent.height

        ListView {
            id: view
            anchors.fill: root
            anchors.margins: 25
//            model: PortfoliosModel
            model: myModel
            delegate: Item {
                width: 180; height: 40
                Column {
                    Text { text: display }
                    Text { text: value }
                }
            }
//            delegate: Row {
//                width: 180; height: 40
//                Column {
//                    Text { text: display }
//                    Text { text: value }
//                }
//            }
            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
            focus: true
        }

    }
}
