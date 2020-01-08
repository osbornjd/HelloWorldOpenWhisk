// This JS FaaS takes an array of strings as a paramter
// and converts it to a string, ultimately printing it to
// a blank webpage. Useful when chained together with
// OpenWhisk split and sort FaaS
function main(params){
    var msg = params.lines.toString();

    return {body: `<html><body><h3>${msg}</h3></body></html>`}
}
