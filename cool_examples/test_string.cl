class Main {
    main() : Int {
	{
	    let io: IO <- new IO,
	        s:String <- "Hola"
	        in
	            io.out_string(s.concat(s.substr(1,s.length()-1)));
	    0;
	}
    };
};