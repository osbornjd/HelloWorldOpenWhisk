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
