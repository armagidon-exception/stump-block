using System;

namespace Namespace
{
    internal class Program
    {
        static void Main(string[] args) {
            //stumpblock-meta-input-start
            double x = 0;
            //stumpblock-meta-input-end
            Math.Sin(0);

            //stumpblock-meta-input-start
            double y = 0;
            //stumpblock-meta-input-end
            Console.WriteLine("Loshara razrabotchik. He ne mog sdelat escho uslovnie operatori");
            bool if_loshara = false;
            if (if_loshara) {
                Console.WriteLine("loshara");
            } else
                Console.WriteLine("ne loshara");
        }
    }
}
