using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace studsched
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComzponent();
        }
        private string[] hereNowList;
        private string[] arrivingSoonList;
        private string[] leavingSoonList;
        public string[] HereNowList
        {
            get { return hereNowList; }
            set
            {
                hereNowList = value;
                hereNowBox.Text = "";
                for (int i = 0; i < hereNowList.Length; i++)
                {
                    hereNowBox.AppendText(value[i] + "\n");
                }
            }
        }
        public string[] ArrivingSoonList
        {
            get { return arrivingSoonList; }
            set
            {
                arrivingSoonList = value;
                arrivingSoonBox.Text = "";
                for (int i = 0; i < arrivingSoonList.Length; i++)
                {
                    arrivingSoonBox.AppendText(value[i] + "\n");
                }
            }
        }
        public string[] LeavingSoonList
        {
            get { return leavingSoonList; }
            set
            {
                leavingSoonList = value;
                leavingSoonBox.Text = "";
                for (int i = 0; i < leavingSoonList.Length; i++)
                {
                    leavingSoonBox.AppendText(value[i] + "\n");
                }
            }
        }

    }
}
