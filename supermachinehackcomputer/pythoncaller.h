#ifndef PYTHONCALLER_H
#define PYTHONCALLER_H

#include <QObject>
#include <QProcess>

class PythonCaller : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString program READ getProgram WRITE setProgram NOTIFY programChanged)

public:
    explicit PythonCaller(QObject *parent = nullptr);

    QString getProgram();
    void setProgram(const QString &progam);


signals:
    void programChanged();
    void programFinished(int exit_code);

public slots:
    void processFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void run(const QString &title, const QString &artist, const QString &bpm, bool shuffle, bool force);

private:
    QString m_program;
};

#endif // PYTHONCALLER_H
