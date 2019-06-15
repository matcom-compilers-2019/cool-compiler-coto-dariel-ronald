class Main {
            main() : Int {
                {
                    case 1+2 of
                        id1:Int => let io: IO <- new IO in io.out_int(id1);
                        id2:Object => let io: IO <- new IO in io.out_string("Es Object");
                        id3:String => let io: IO <- new IO in io.out_string(id3);
                    esac;
                    let a:Object <- 42, io: IO <- new IO in io.out_string(a.type_name());
                   5;
               }
            };
        };
