const _ = require("lodash")


var Data =
{
    time:[1,2,3],
    price:[1,2,3,4,5,6,7,8],
    volume:[1,2,3],
    low:[1,1,1],
    high:[3,3,3],


    now:0,
    last:2
}

const info = {
    momentumUpper:1.2,
    momentumLower:0.97
}

function netReturn(price){
    var prev = price[0]
    return _.map(price, function(v){
        res = v / prev
        prev = v
        return res
    })
}

function momentumForSell(data, n){
        var lReturn = netReturn(data)
        var comp = _.reduce(lReturn, function(res,arr){ return res * arr}, 1)
        if ( comp < info.momentumLower )
            return True
        else
            return False
}

function momentumForBuy(data, perd){
        var lArr = _.takeRight(data,per)
        var lReturn = netReturn(lArr)
        var comp = _.reduce(lReturn, function(res,arr){ return res * arr}, 1)
        if ( comp > info.momentumUpper )
            return true
        else
            return false
}

function Criterion(data,bcrit,perd){
    return bcrit(data,perd)()
}

function MomentumBuyCrit(data,n){
    return momentumForBuy(data,n)
}


module.exports{
    momentumBuyCrit : MomentumBuyCrit
}
