
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 2.12

//import PortfoliosModel

Page {
    width: 640
    height: 480
    required property var mainModel

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
    RowLayout {
        anchors.fill: parent
        Rectangle {
            id: navigationRoot
            color: '#fff'
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.minimumWidth: 50
            Layout.preferredWidth: 100
            Layout.maximumWidth: 300
            Layout.minimumHeight: 150

            ListView {
                id: view
                anchors.fill: navigationRoot
                anchors.margins: 25
    //            model: PortfoliosModel
                model: mainModel
                delegate: Component {
                    id: navItemWrapper
                    Rectangle {
                        color: ListView.isCurrentItem ? "#e2e2e2" : "#ffffff"
                        height: 40
                        Item {
                            id: navItem
                            width: view.width
                            height: 40
                            focus: true

                            Text {
                                text: display
                                anchors.verticalCenter: parent.verticalCenter
                                padding: 10
                            }
                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                acceptedButtons: Qt.LeftButton
    //                            onExited: navItemWrapper.color = "#fff"
    //                            onEntered: navItemWrapper.color = "#e2e2e2"
                                onClicked: (mouse)=> {
                                    view.model.selectPortfolio(identifier)
                                }
                            }
                        }
                    }
                }
                focus: true
            }
        }
        Rectangle {
            id: contentRoot
            objectName: "contentRoot"
            color: '#fff'
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.minimumWidth: 100
            Layout.preferredWidth: 200
            Layout.preferredHeight: 100
            Text {
                text: "Portfolio"
            }
            PortfolioView {}
        }
    }
}
