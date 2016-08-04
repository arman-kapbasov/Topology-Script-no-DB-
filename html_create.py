nl='''
'''


def html_intro(filename, page):
    f = open(filename + '.html', 'w')
    str1 = '''
    {% extends "empire/index.html" %}
    {% block selected_scaling %}class="current"{% endblock %}
    {% block page_content %}
    <div class="content">
    <script type="text/javascript">
        function swap(targetId){
          if (document.getElementById){
            target = document.getElementById(targetId);
            if (target.style.display == "none"){
                target.style.display = "";
            } else{
                target.style.display = "none";
            }
        }
    }
    </script>
    <title>
    '''

    str2 = '''
    </title>
    </head>
    <body style="padding:10">
    <style>

    .center {
        margin: auto;
        width: 50%;
    }
    pre{
        padding-left: 140px;
        color: #59b4a1;
        font-size: 150%;
        font-family: monospace;
        }
    </style>
    <script src="http://canvasjs.com/assets/script/canvasjs.min.js"></script>

    '''
    f.write(str1)
    f.write(page)
    f.write(str2)

    f.close()


def html_writeDirectly(filename, string):
    f = open(filename + '.html', 'a')
    f.write(string)
    f.close()


def html_main_head(filename, page, dash, summary, opti, all_topo):
    f = open(filename + '.html', 'a')
    str1 = '''
        <div class="filters">
          <table>
            <tr>
                <th>
                    <div class="dropdown cf">
                        <a href="#">Topology Navigation: <span id="drop_metric" class="current">'''
    str1a = '''</span></a>
                        <div>
                            <a class="icosolo icon_arrow_down" href="#"></a>
                            <ul>
                                    '''
    str2 = '''<li><a href="/empire/'''
    str3 = '''">'''
    str4 = '''</a></li>'''
    str5 = '''
                            </ul>
                       </div>
                   </div>
               </th>
           </table>
    </div>'''
    f.write(str1)
    f.write(page)
    f.write(str1a)
    f.write(str2)
    f.write(dash)
    f.write(str3)
    f.write("Dashboard")
    f.write(str4)

    f.write(str2)
    f.write(summary)
    f.write(str3)
    f.write("Summary")
    f.write(str4)

    f.write(str2)
    f.write(opti)
    f.write(str3)
    f.write("Optimization")
    f.write(str4)

    f.write(str2)
    f.write(all_topo)
    f.write(str3)
    f.write("Topology Listing")
    f.write(str4)

    f.write(str5)
    f.write(nl)
    f.close


def html_pagetitle(filename, pagetitle):
    f = open(filename + '.html', 'a')
    str_h1 = '<div class="page_title">'
    str_h2 = "</div>"

    f.write(str_h1)
    f.write(pagetitle)
    f.write(str_h2)

    f.close()


def html_header(filename, header, size, location):
    f = open(filename + '.html', 'a')
    if location is 1:
        str_h1 = '<h' + str(size) + ' align="center" >'
        str_h2 = "</h" + str(size) + ">"
    else:
        str_h1 = "<h" + str(size) + ' style="margin-left: 8px" > '
        str_h2 = "</h" + str(size) + ">"

    f.write(str_h1)
    f.write(header)
    f.write(str_h2)

    f.close()


def html_paragraph(filename, paragraph, flag):
    f = open(filename + '.html', 'a')
    str_p1 = ' <p1 style="margin-left: 8px" >'
    str_p2 = "</p1 >"

    if(flag):
        f.write("<blockquote>")
    f.write(str_p1)
    f.write(paragraph)
    f.write(str_p2)
    f.write(nl + "<br>")
    if(flag):
        f.write("</blockquote>")

    f.close()


def html_paragraphCenter(filename, paragraph):
    f = open(filename + '.html', 'a')
    str_p1 = '<p align="center">'
    str_p2 = "</p1 >"

    f.write(str_p1)
    f.write(paragraph)
    f.write(str_p2)
    f.write(nl + "<br>")

    f.close()


def html_paragraph_color(filename, paragraph, flag):
    f = open(filename + '.html', 'a')
    str_p1 = ' <p1 style="margin-left: 8px;color: #59b4a1;" >'
    str_p2 = "</p1 >"

    if(flag):
        f.write("<blockquote>")
    f.write(str_p1)
    f.write(paragraph)
    f.write(str_p2)
    f.write(nl + "<br>")
    if(flag):
        f.write("</blockquote>")

    f.close()


def html_pI(filename, paragraph, flag):
    # paragraph with pre defined spacing
    f = open(filename + '.html', 'a')
    str1 = '''<pre><p5>'''
    str2 = '</p5></pre>'

    if(flag):
        f.write("</blockquote>")

    f.write(str1)
    f.write(paragraph)
    f.write(str2)
    #f.write(nl + "<br>")

    if(flag):
        f.write("</blockquote>")

    f.close()


def html_collapse_start(filename, title, num, extra_info):
    # title is the title of the button and num is the unique num
    f = open(filename + '.html', 'a')
    str1 = '''
        <div class="tab" id="navigation">
                <a href="#" class="button" onclick="swap('test'''
    str2 = '''');return false;">
    '''
    if extra_info:
        str3 = '''
            </a>'''
        str4 = '''
            <div class ="tab" id="test'''

        str5 = '''" style="display: none;">
        '''

        f.write(str1)
        f.write(str(num))
        f.write(str2)
        f.write(title)
        f.write(str3)
        f.write("<br>")
        f.write("<br>")
        f.write("<blockquote>")
        f.write(str(extra_info))
        f.write("</blockquote>")
        f.write(str4)
        f.write(str(num))
        f.write(str5)
    else:
        str3 = '''
            </a>
            <div class ="tab" id="test'''

        str4 = '''" style="display: none;">
        '''

        f.write(str1)
        f.write(str(num))
        f.write(str2)
        f.write(title)
        f.write(str3)
        f.write(str(num))
        f.write(str4)

    f.close()


def html_collapse_middle(filename, content):
    f = open(filename + '.html', 'a')

    f.write(content)
    f.close()


def html_collapse_end(filename):
    f = open(filename + '.html', 'a')
    str1 = '''
        </div>
        </div>
    '''
    f.write(str1)
    f.close()


def html_graphStart(filename):
    f = open(filename + '.html', 'a')
    str1 = '''
         <script type="text/javascript">
         window.onload = function () {
             CanvasJS.addColorSet("aruba",
                [
                "#2F4F4F",
                "#008080",
                "#2E8B57",
                "#3CB371",
                "#90EE90"
                ]);'''
    f.write(str1)

    f.close()


def html_graphScript(filename, graphID, ar_data1, data_name1,
            ar_data2, data_name2, title, chart):
    f = open(filename + '.html', 'a')
    str1 = '''
          var chart = new CanvasJS.Chart("chartContainer'''
    str2 = '''",
          {
           theme: "theme1",
           colorSet: "aruba",
                                animationEnabled: true,
           title:{
            text: "'''
    str3 = '''",
            fontSize: 20
           },
           toolTip: {
            shared: true
           },
               data: [
    '''
    strData = '''
        {
            type: "'''
    strPercent = '''",
            indexLabel: "{label} {y}'''
    strIndexLabel = '''",
            toolTipContent:"{legendText} {y}'''
    strChartType = '''",
            name: "'''
    dataName1a = '''",
            legendText: "'''
    dataName1b = '''",
            showInLegend: true,
            dataPoints:['''
    labelName = '''
            {label: "'''
    label_legend = '''", legendText: "'''
    labelValue = '''", y: '''
    labelend = '''},
        '''
    dataEnd = ''']
          },'''
    strend = '''],

                });

        chart.render();
    '''
    f.write(str1)
    f.write(str(graphID))
    f.write(str2)
    f.write(str(title))
    f.write(str3)

    if ar_data1:
        f.write(strData)
        f.write(str(chart))
        if "pie" in chart:
            f.write(strIndexLabel)
            f.write("%")
            f.write(strPercent)
            f.write("%")
        f.write(strChartType)
        f.write(data_name1)  # user defined data name
        f.write(dataName1a)
        f.write(data_name1)  # user defined data name
        f.write(dataName1b)
        for x in xrange(0, len(ar_data1), 2):
            f.write(labelName)
            f.write(str(ar_data1[x]))
            if "pie" in chart:
                f.write(label_legend)
                f.write(str(ar_data1[x]))
            f.write(labelValue)
            f.write(str(ar_data1[x + 1]))
            f.write(labelend)
        f.write(dataEnd)
    if ar_data2:
        f.write(strData)
        f.write(str(chart))
        f.write(strChartType)
        f.write(data_name2)  # user defined data name
        f.write(dataName1a)
        f.write(data_name2)  # user defined data name
        f.write(dataName1b)
        for x in xrange(0, len(ar_data2), 2):
            f.write(labelName)
            f.write(str(ar_data2[x]))
            if "pie" in chart:
                f.write(label_legend)
                f.write(str(ar_data2[x]))
            f.write(labelValue)
            f.write(str(ar_data2[x + 1]))
            f.write(labelend)
        f.write(dataEnd)

    f.write(strend)

    f.close()


def html_graphEnd(filename):
    f = open(filename + '.html', 'a')
    str1 = '''}
        </script>'''
    f.write(str1)

    f.close()


def html_graph(filename, graphID, height, width):
    f = open(filename + '.html', 'a')
    str1 = '''
    <div id="chartContainer'''
    str2 = '''" class="center" style="height: '''
    strH = '''px; width: '''
    strW = '''%;">
    </div>'''
    f.write(str1)
    f.write(str(graphID))
    f.write(str2)
    f.write(str(height))
    f.write(strH)
    f.write(str(width))
    f.write(strW)

    f.close()


def html_table_start(filename, list1):
    f = open(filename + '.html', 'a')
    str1 = '''
        <div class = "panel_wrapper">
        <div class = "panel table rounded white no_pad">
        <div class = "table_wrapper">
        <font size="3">
        <table class="data selective">
      '''
    str3 = "<th>"
    str4 = "</th>"
    str5 = "</tr> <tr>"

    f.write(str1)
    for entry in list1:
        f.write(str3)
        f.write(entry)
        f.write(str4)
    f.write(str5)
    f.close()


def html_table_mid(filename, data, boxID):
    f = open(filename + '.html', 'a')
    str1 = '''
        <td><output id="tableBox'''
    str2 = '''" />'''
    str3 = '''</output></td>
        '''

    f.write(str1)
    f.write(str(boxID))
    f.write(str2)
    f.write(str(data))
    f.write(str3)
    f.close()


def html_table_script(filename, scriptID, inputID, dic_ID):
    f = open(filename + '.html', 'a')
    str1 = '''
    <script>
        function calculate'''
    str2 = '''(){
        var data;
        var cons;
        var result;'''
    str3 = '''
            cons = document.getElementById("input'''
    str4 = '''").value;
            data = '''
    str5 = '''
            result = document.getElementById('tableBox'''
    str6 = '''');
            result.value = cons * data;
        '''
    str7 = '''
        }
        </script>'''
    f.write(str1)
    f.write(str(scriptID))
    f.write(str2)

    for ID in dic_ID:
        f.write(str3)
        f.write(str(inputID))
        f.write(str4)
        f.write(str(dic_ID[ID]))
        f.write(str5)
        f.write(str(ID))
        f.write(str6)
    f.write(str7)
    f.close()


def html_table_mid2(filename, data, flag_script, inputID, scriptID,
            boxID, default):
    # parameters: flag_script is the flag for addind script
    # inputID is the input box ID, scriptID is the scriptID, boxID is current
    # default is the constant to be multiplied
    f = open(filename + '.html', 'a')
    str1 = '''
    <td>
    '''
    str2 = "</td>"
    # value that is outputed at first
    default1 = default * data
    if flag_script:
        str1 = '''
        <td><output id="tableBox'''
        str2 = '''" />'''
        str3 = '''</output></td>
        '''
        f.write(str1)
        f.write(str(boxID))
        f.write(str2)
        f.write(str(default1))
        f.write(str3)

    else:
        str1 = '''<style> input[type=number]{width: 50px;} </style>
        <td><input type="number" id="input'''
        str2 = '''" step=".5" min = "1" max="20" value="'''
        str3 = '''" oninput="calculate'''
        str3a = '''()" />'''
        str4 = '''</td>'''
        f.write(str1)
        f.write(str(inputID))
        f.write(str2)
        f.write(str(default))
        f.write(str3)
        f.write(str(scriptID))
        f.write(str3a)
        f.write(" mins")
        f.write(str4)
    f.close()


def html_table_end(filename):
    f = open(filename + '.html', 'a')
    str1 = '''
        </tr>
        </table>
        </font>
        </div>
        </div>
        </div>
    '''
    f.write(str1)
    f.close()


def html_break(filename):
    f = open(filename + '.html', 'a')
    f.write(nl + "<br>")
    f.close()


def html_line(filename):
    f = open(filename + '.html', 'a')
    f.write(nl + "<HR>")
    f.close()


def html_line_small(filename):
    f = open(filename + '.html', 'a')
    f.write(nl + "<HR width='50%'>" + nl)
    f.close()


def html_end(filename):
    f = open(filename + '.html', 'a')

    str1 = '''
    </div>
    {% endblock %}
    '''
    f.write(str1)
    f.close()