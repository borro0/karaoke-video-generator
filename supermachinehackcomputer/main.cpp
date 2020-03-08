#include <QApplication>
#include <QQuickView>
#include <QUrl>
#include <QQuickItem>
#include "pythoncaller.h"

int main(int argc, char *argv[])
{

    QApplication app(argc, argv);
    QQuickView view;

    qmlRegisterType<PythonCaller>("CustomTypes", 1, 0, "PythonCaller");

    view.setSource(QUrl("qrc:/main.qml"));
    view.setResizeMode(QQuickView::SizeRootObjectToView);
    view.show();
    return app.exec();
}
