const Pty = require('node-pty');
const fs = require('fs');

const WIDTH = process.env.WIDTH != null ? process.env.WIDTH : 80;
const HEIGHT = process.env.HEIGHT != null ? process.env.HEIGHT : 24;

exports.install = function () {

    // Route to views/index
    ROUTE('/');

    // WebSocket route
    WEBSOCKET('/', socket, ['raw']);

};

function socket() {

    var self = this;

    self.encodedecode = false;
    self.autodestroy();

    self.on('open', function (client) {

        // Each client will have own terminal
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',
            cols: WIDTH,
            rows: HEIGHT,
            cwd: process.env.PWD,
            env: process.env
        });

        client.tty.on('exit', function (code, signal) {
            // What now?
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function (data) {
            client.send(data);
        });

    });

    self.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    self.on('message', function (client, msg) {
        client.tty && client.tty.write(msg);
    });
}

if (process.env.CREDS != null) {
    fs.writeFile('creds.json', process.env.CREDS, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
            socket.emit("console_output", "Error saving credentials: " + err);
        }
    });
}