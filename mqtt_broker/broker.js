var mosca = require('mosca');
var fs = require('fs');
var path = require('path');
require('dotenv').config();

const { networkInterfaces } = require('os');

const nets = networkInterfaces();
const results = Object.create(null); // Or just '{}', an empty object

for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
        // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
        if (net.family === 'IPv4' && !net.internal) {
            if (!results[name]) {
                results[name] = [];
            }
            results[name].push(net.address);
        }
    }
}

console.log(" * WiFi IP:" , results["Wi-Fi"][0]);

var settings = {
    port: 1883,
    http: {
    port: 8883,
    static: './templates'
    }
    };

var client_data = []
var paths = path.join(__dirname)
fs.writeFile(paths +"/client_data.json", JSON.stringify(client_data), function (err) {
    if (err) throw err;
    console.log(' * initial client_data Ok');
    });

var server = new mosca.Server(settings); //สร้างตัวแปรมารับค่า server
server.on('ready', setup); //ใช้คำสั่ง ready,setup เพื่อตั้งค่า
function setup() {
    server.authenticate = authenticate; // ตั้งให้เซิพเวอร์ต้องมี Authen สามารถ เปิดคอมเม้นได้หากต้องการกำหนดการใช้งานระหัสผ่าน
    console.log(' * Mosca server is up and running MQTT_BROKER')
    console.log(' * listening on port:',settings);
}

var authenticate = function (client, username, password, callback) {//Athentication configuration
    var authorized = (username === "ats&p" && password.toString() === "ats&p2020");
    if (authorized) client.user = username;
    callback(null, authorized);
}

server.on('clientConnected', function (client) {
    console.log('Client Connected:', client.id);
});

server.on('clientDisconnected', function (client) {
    console.log('Client Disconnected:', client.id);

    for(var i = 0;i < client_data.length;i ++){
        if(client_data[i].socket_id == client.id){
         client_data.splice(i,1);
        }
    }
    
    fs.writeFile(paths + "/client_data.json", JSON.stringify(client_data), function (err) {
        if (err) throw err;
        console.log('Updated client data');
        });

});

var file = path.basename(paths + "/client_que.json");
var i_count = 0;

server.subscribe("inav1", (topic, message) =>{ //รับค่าจาก "inav1"
    try{
        fs.readFile(file, function(err, data) { //อ่านข้อมูลจากที่อยู่ไฟล์
            var jsonObj = JSON.parse(data.toString()); //แปลงข้อมูลจาก Json เป็น String
            for(var i = 0;i<jsonObj.length;i++){ //เงื่อนไข
            if(jsonObj[i].name == "inav1"){ //ถ้าเงื่อนไขเท่ากับ inav1
            console.log("name : ",jsonObj[i].name);
            console.log("que : ",i);
            var packet = {
                topic: "inav1/rcv", //ส่งค่าไปยัง "inav1/rcv"
                payload: JSON.stringify({"name":"inav1","que":String(i),"count":String(i_count)}),
                qos: 1,
                retain: false,  
              };
        
              server.publish(packet, function() {
                console.log('MQTT broker message sent');
              });
              i_count ++;
            }
            }
            });
         }
        catch(err){
        console.log(error);
     }

//console.log(message.toString());
});


var raw_subscripe = ""
server.on('published', function (packet, client) {
    //console.log(packet);
    if(i_count>99){
        i_count = 0;
    }
    raw_subscripe = packet.payload.toString();
    try {//============================================================================================check client login
        var raw_data = packet.payload.toString();
        var data = JSON.parse(raw_data)
        if(data.dev_name != undefined){
            var client_detail = {
                client_name:data.dev_name,
                socket_id:client.id
               }
            client_data.push(client_detail);
            fs.writeFile("client_data.json", JSON.stringify(client_data), function (err) {
               if (err) throw err;
               console.log(' * client login :  Ok');
               });
        // console.log("device name:",data.dev_name,"  ","socket_id:",client.id);
         fs.close();
        }
    } catch (error) {
    }
        //============================================================================================check client login
    console.log('Client Published <=>', packet.payload.toString());

   // check_alive(packet.payload.toString());
    call_que(packet.payload.toString());

    });

var que_buffer = [];
function call_que(packet){
    try {
        var json_pack = JSON.parse(packet);
        if(json_pack.time != undefined){ 
        console.log("time:",json_pack.time);
        if(json_pack.control == "add"){

            var data = {
                name:json_pack.name,
                time:json_pack.time,
                control:json_pack.control
               }

            que_buffer.push(data);
            console.log("control:",json_pack.control);

        }
        if(json_pack.control == "remove"){
         for(var i=0;i<que_buffer.length;i++){
             if(json_pack.name == que_buffer[i].name){
                que_buffer.splice(i,1);
             }
            }
        }

        fs.writeFile(paths + "/client_que.json", JSON.stringify(que_buffer),function (err) {
            if (err) throw err;
            return console.log('Update que : Ok',que_buffer);
            });
        fs.close();
    }
    } catch (error) {
        console.log(error.message);
    }
    }

function check_alive(packet){
    try {
        var json_pack = JSON.parse(packet);
        if(json_pack.name != undefined && json_pack.check != undefined){
        console.log("name:",json_pack.name,"check:",json_pack.check); 
        }
    } catch (error) {
        
    }
    }