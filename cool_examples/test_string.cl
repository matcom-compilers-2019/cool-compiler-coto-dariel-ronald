class Main {
    main() : Int {
	{
	    let io: IO <- new IO,
	        s:String <- "Hola"
	        in
	            io.out_string(s.concat(s.substr(1,s.length()-1)));
	    let io: IO <- new IO in
	        if true
	        then io.out_string("es prefijo")
	        else io.out_string("no es prefijo") fi;
	    0;
	}
    };
};