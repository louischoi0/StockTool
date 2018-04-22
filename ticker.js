const rq = require("request")
const redis = require("redis")
const sqlite3 = require("sqlite3").verbose()
const DBDIR = "./data/sci.db"
const _ = require("lodash")
const crit = require("./ticker.js")
const CODES = [ "BTC", "EOS"]

const MAX = 2000
var COUNT = 0
var avArr = []

const UTICKER = {
    bitthumb:"https://api.bithumb.com/public/ticker/"
}

let DB = new sqlite3.Database(DBDIR, sqlite3.OPEN_READWRITE);

const MOMENTUMP = 10

const ex = {"opening_price":"9100000","closing_price":"9579000","min_price":"8820000","max_price":"9669000","average_price":"9200377.4385","units_traded":"15233.62591735","volume_1day":"15233.62591735","volume_7day":"82821.73363404","buy_price":"9579000","sell_price":"9584000","date":"1524279273648" }

function Columns(arr){
    var idx = 0
    var cols = ""
    _.forOwn(arr, function(vals,key){
            if ( idx == 0 )
                cols += "(";

            if ( idx != _.size(arr) - 1)
                cols += key + ",";
            else
                cols += key + ")";

            idx++; })
    return cols
}

const columns = Columns(ex)

function Values(arr){
    var vals = ""
    var idx = 0

    _.map(arr, function(v){
        if ( idx == 0 )
            vals = "VALUES("
        if ( idx != _.size(arr) - 1 )
            vals += v + ","
        else
            vals += v + ")"
        idx ++
    })
    return vals
}


function insert(data,db, code){
    var QUERY = "INSERT INTO "+ code + columns + Values(data)
    db.run(QUERY)
    console.log("inserted : " + code)
}

async function ticker(code){
    await rq({
            uri: UTICKER.bitthumb + code,
            method: "GET",
            timeout: 10000,
            followRedirect: true,
            maxRedirects: 10 }, function(error, res, body){
                var res = JSON.parse(body)
                insert(res.data, DB, code)
                toLocalAvg(res.data)
            })
}

function tickerTask(codes){
        return function() { _.map(codes,function(code){ ticker(code) }) }
}

function main(){
    setInterval( tickerTask(CODES), 1000)

}


function toLocalAvg(data){
    if ( COUNT < MAX ) {
        avArr.pop()
    }

    avArr.push(data.average_price)
}

function investigate(data){
        if ( _.size(data) < MOMEUTNP )
            return False

        return crit.momentumBuyCrit(data, MOMENTUMP)

}



main()
