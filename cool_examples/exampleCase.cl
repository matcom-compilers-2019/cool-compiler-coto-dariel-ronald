class Main {
            main() : Object {
                while true loop
               {
                    case 1+2 of
                        id1:Int => id1+5;
                        id2:Object => id2;
                        id3:String => id3;
                    esac;
                    if 2<=3 then
                    {
                        let io: IO <- new IO in io.out_string("True");
                    }
                    else {
                        let io: IO <- new IO in io.out_string("False");
                    }
                    fi;
               } pool
            };
        };
        class A {
            attr1:Int<-24;
            attr1() : Int {attr1};
            method2():Int {attr1()};
            method3(index:Int):Int {
                if index = 0 then method2() else {
                        let io: IO <- new IO in io.out_string("Call method3");
                        method3(index - 1);
                    }
                fi
            };
        };