/**
 * This function takes in a name and a separator and is intended to be
 * chained together with other string parsing functions. 
 */

function main(params){
    var msg = 'you did not tell me who you are';
    if(params.name) {
	msg = `hello ${params.name}!`;
    }

    var sep = '\n';
    if(params.separator){
	sep = `${params.separator}`;
    }

    return {payload: msg,
	    separator: `${sep}`
	   };
    
}
