   class Main {
    main() : Int {
            {
                let io: IO <- new IO in io.out_string("Hello \
                                                        World\n");
                let a:A <- new B, b: Int in
                                        let i:Int <- a.funk(1) + b, io: IO <- new IO in io.out_int(i);
                0;
                (*asasdadadad*)
            }
        };
    };
    class A {
       attr1:Int<-22;
       funk():Int {
            let x:Int in x + 1
       };
    };
    class B inherits A {
        attr2:Int <-5;
        funk(input1:Int):Int {
            {   while 1 = attr2  loop
                {
                    attr2 <- attr2 - input1;
                    let io: IO <- new IO in io.out_int(attr2);
                } pool;
                attr2;
            }
        };
    };
    class C {
        attr1:Int<-0;
        funk():Int {
            32
        };
    };

