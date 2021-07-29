using System;
using System.ComponentModel;
using System.Reflection;
using System.Linq;

namespace RsFsw_Basic_TraceAcquisition_Example
{
    class Program
    {
        [Description("HasCustomStrings")]
        public enum Janik
        {
            Ferdo1,
            [Description("TotoJeJarda")]
            Jardo2,
            OpenFire3
        }

        public enum JanikEmpty
        {
            Ferdo1,
            [Description("TotoJeJarda")]
            Jardo2,
            OpenFire3
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            var b = typeof(JanikEmpty).GetCustomAttributes(typeof(DescriptionAttribute), false);

            var a = Janik.Jardo2.GetDescription();
            var c = Janik.OpenFire3.GetDescription();

        }
    }

    public static class Extensions
    {
        public static string GetDescription(this Enum e)
        {
            var x = e.GetType()
                    .GetTypeInfo().GetMember(e.ToString());
            var attribute =
                e.GetType()
                    .GetTypeInfo().
                    GetMember(e.ToString())[0]
                    .GetCustomAttribute(typeof(DescriptionAttribute), false)
                    as DescriptionAttribute;

            return attribute?.Description ?? e.ToString();
        }
    }

}
