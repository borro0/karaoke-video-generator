#include "pythoncaller.h"

#include <QObject>
#include <QString>
#include <QProcess>
#include <QDebug>

PythonCaller::PythonCaller(QObject *parent)
    : QObject(parent)
{
}

QString PythonCaller::getProgram()
{
    return m_program;
}

void PythonCaller::setProgram(const QString &program)
{
    if (m_program != program)
    {
        m_program = program;
        emit programChanged();
    }
}

QString buildBpmString(const QString &bpm, bool shuffle)
{
    if (shuffle)
    {
        return QStringLiteral("%1S").arg(bpm);
    }
    else
    {
        return QStringLiteral("%1bpm").arg(bpm);
    }
}

QStringList buildArgumentList(const QString &program, const QString &title, const QString &artist, const QString &bpm, bool shuffle, bool force)
{
    QStringList arguments;
    QString s_bpm = buildBpmString(bpm, shuffle);
    arguments << program << title << artist << s_bpm;
    if (force)
    {
        arguments << "--force";
    }

    return arguments;
}

void PythonCaller::processFinished(int exitCode, QProcess::ExitStatus exitStatus)
{
    qDebug() << "program finished: " << exitCode << exitStatus;
    emit programFinished(exitCode);
}

void PythonCaller::run(const QString &title, const QString &artist, const QString &bpm, bool shuffle, bool force)
{
    QString program = "python";

    QStringList arguments = buildArgumentList(m_program, title, artist, bpm, shuffle, force);

    qDebug() << program << arguments;

    QProcess *myProcess = new QProcess(this);
    connect(myProcess , SIGNAL(finished(int,QProcess::ExitStatus)), this, SLOT(processFinished(int, QProcess::ExitStatus)));
    myProcess->start(program, arguments);
}
