# Otto DIY

Otto is truly Opensource robot for education; it means the hardware is easily discerned so that others can make it, is also Arduino compatible, 3D printable and customizable, the perfect opportunity to build and have your very first robot, learn robotics and have fun, you will learn the logical connection between code and action, and by assembling it, you will understand how its components and electronics work.

Visit our website www.ottodiy.com for more detailed info.

This Repository have all source including 3D design, 3D print files, libraries, Arduino code, how to guides, instruction manuals and even some papercrafts to personalize your own robot .

## How it Works

Otto walks, dances, makes sounds and avoids obstacles, easy to program and expand or customize by your own.
![Otto DIY features](https://alpha.wikifactory.com/files/RmlsZTo0NDg5)
@[watch youtube video](https://youtube.com/embed/VD6sgTo6NOY)

In the basic form Otto walks, dances, makes sounds, easy to program with blockly, avoids obstacles, expandable or you can customize by your own. Thanks to the active community contributions now is a big family of multifunctoinal robots, that you can also make but [please make sure to refer to their specific documentation here](https://wikifactory.com/+OttoDIY/projects) since there are variations that might use different materials, files, instructions or codes than this one.

## Build Your Own Robot

> ### Otto DIY can be made with [Builder Kit \(full with 3D printed parts\)](https://ottodiy.ecwid.com/Otto-DIY-Builder-Kit-p135022769)  and [Maker Kit \(only electronics\)](https://ottodiy.ecwid.com/Otto-DIY-Maker-Kit-p135022782) or create your own project with this open source content.

## Part List

Here there is a list of the materials you will need to build the BASIC Otto.
![image](https://user-images.strikinglycdn.com/res/hrscywv4p/image/upload/c_limit,fl_lossy,h_9000,w_1200,f_auto,q_auto/838564/OttoDIY_officialtobotbuilderkit_lzdp7r.jpg)

* 1 x Nano ATmega328
* 1 x Nano I/O shield
* 1 x USB-A to Mini-USB Cable
* 1 x Ultrasound sensor HC-SR04
* 4 x Micro servo SG90 9g
* 1 x Piezo Buzzer
* 6 x Female/Female Dupont Wires
* 1 x AAbattery holder
* 4 x AA Batteries Alkaline \(must be new or have 1.5V each\)
* 1 x Micro Switch Self lock On/Off 8x8mm
* [3D printed head](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/3Dprint/OttoDIY%2B_head_V9.stl)
* [3D printed body](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/3Dprint/OttoDIY%2B_body_V9.stl)
* [3D printed leg x2](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/3Dprint/OttoDIY%2B_Leg_V9.stl)
* [3D printed foot x2](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/3Dprint/OttoDIY%2B_foot_V9.stl)

**Tools:**

* Small Phillips screwdriver.
* Computer.
* Scissors or pliers.
* 3D Printer

## 3D Printing

If you bought a **Builder kit** you can skip ahead but if you have the **Maker kit** you have to[ 3D print the main parts ](https://github.com/Open-Hardware-Leaders/OttoDIY/tree/master/3Dprint)but do not worry, Otto is very well designed for easy 3D printing, so wont give you trouble if you follow this common parameters:

* Recommended to use a FDM 3D printer with PLA material.
* No need supports or rafts.
* Resolution: 0.20mm or even 0.3mm is still fine in most cases
* Fill density at least 20%

All parts in total use 115gr aprox. equivalent to 14.5m of regular PLA 1.75mm thickness, it should take around **8 hours to 3D print** a full set of parts for one Otto even less with a proper 3D printer and optimized settings.

As with any fabrication technology you might adjust to desire quality and speed or share with us some better ways to optimize.

## Software

### For **beginners** it is recommended to start coding by using our new Blockly a simple visual programming software:

Otto Blockly is completely autonomous \(no need for Arduino IDE, or libraries setup and no Internet access is required\).
![image](https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.ottodiy.com%2Fblog%2Fottodiykit&psig=AOvVaw0qNNFY2UVLLNSvmjJBLcAD&ust=1585233443461000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLDt0_bstegCFQAAAAAdAAAAABAF)

1. [Download from our website here](https://www.ottodiy.com/#blockly)
2. Unzip and install OttoBlockly.
3. Open an example.
4. Connect your Otto robot.
5. Select Arduino nano, **USB port where Otto is connected.**
6. Check the code.
7. Upload and yes is that easy!

@[youtube](https://youtube.com/embed/chcWxh4Co_c)

[Make sure to also follow the Blockly guide](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/How%20to%20guides/OttoBlocklyguide.pdf)

**If your computer did not recognize the USB device you should [install the driver CH340 for your Operative System find it here:**](https://sparks.gogo.co.nz/ch340.html)

Play with the examples and start mixing blocks in multiple ways to decide the behaviour of your robot and generate your own codes.
[We also have our educational content open for FREE, learn about robotics and help us creating more lessons here.]
(https://wikifactory.com/+OttoDIY/open-edu)

---

### For **more advanced** Arduino programming follow our [coding guide](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/How%20to%20guides/OttoDIY_codingguide_V9.pdf) from the files tab folder, it will allow you to really exploit the potential of your robot, you will be able to try more than 15 examples sketchs that you can just simply upload and modify the source for your own ideas.

1. [Download the software for free here Arduino IDE \(version 1.8.5\)](https://www.arduino.cc/en/Main/OldSoftwareReleases#previous)
2. InstallArduino IDE software.
3. Download all the libraries from the files tab and unzip in your libraries folder \(for example C:\Users\user\Documents\Arduino\libraries\)
4. Connect your Arduino Nano through USB make sure the driver CH340 is installed in your computer by checking is in COM\#
5. Open one of the code examples [in the code folder](https://github.com/Open-Hardware-Leaders/OttoDIY/tree/master/Code)
6. Upload the code and check that everything is working.

## Electronics

### **Before inserting the AA batteries you should check your connections and test your robot with the USB cable connected to a computer.**

As a good practice you should check your electronics and software in your computer, before assembling all the robot, this avoid having to disassemble the whole robot to fix something. You can do this by just connecting all the servos, in the place indincated in the wring below **and upload any code** that makes Otto move with Otto Blockly or Arduino.

![image](https://wikifactory.com/files/RmlsZToyODQ0Mjg=)

If you feel ready for Batteries you can also check if your power source works, depending of the type of cells you have there can be 2 options:

![image](https://wikifactory.com/files/RmlsZToyODQ0MjY=)

![image](https://wikifactory.com/files/RmlsZToyODQ0Mjc=)

[There are actually plenty options to power your Otto robot in multiple ways, we explore in more detail in this blog post article](https://www.ottodiy.com/blog/power)

## Assembly Instructions

Gather all the off the shelf hardware parts that you'll need for this assembly, or start with our full kits which come with all parts needed. [Kits are available from our e-shop](https://ottodiy.ecwid.com/)

Before getting started with the assembly, download and read carefully this [PDF instruction manual](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/How%20to%20guides/OttoDIY_Manual_V9.pdf)

If you do not understand something in the manual you can just refer to this video that shows how to build Otto.

@[watch the complementary youtube how to video](https://youtube.com/embed/34v7R0FrSNE)

If you see some missaligment in the movements, double check that you centered the arms repect to your servos before fixing with the short screw, but if you want more precise walk and movements, then you can do some electronic calibration as [we explain in detail in this blog article](https://www.ottodiy.com/blog/calibration)

## Customize

Download, print, cut and make papercrafts of Otto to personalize your robot.

Or if you wanna learn 3D modeling Otto is design using [TinkerCAD ](https://www.tinkercad.com/users/h8O1zJQboeH-camilo-parra-palacio)a FREE 3D modeling online software! , you can modify Otto parts for further improvements or create new accessories for new features.

![image](https://wikifactory.com/files/RmlsZToyNDE2NzM%3D)

Read this blog post to learn more options of [how to redesign your own robot](https://www.ottodiy.com/blog/design)

## Join the Otto Builder community!

Follow us, subscribe, give us a like and share your creativity.Be a part of this friendly community of robot builders, teachers and makers!

1. [Join us in Wikifactory](https://wikifactory.com/invite/SW52aXRlTGluazo3Ng/ZzHGYHg9oAwik0u-vJrz-x0fsEWrONV54SaYpNx9t1A) [Check our Forum for any questions](https://wikifactory.com/+OttoDIY/forum)
2. [Group in Facebook](https://www.facebook.com/groups/ottodiy/). to share and ask for help in the community and like our [Facebook page](https://www.facebook.com/ottodiy/)
3. [YouTube channel](https://www.youtube.com/c/ottodiy?sub_confirmation=1) for more how to videos and tutorials.
4. [Instagram](https://www.instagram.com/ottodiy/) to share \#ottodiy
5. [Twitter](https://twitter.com/ottodiy) to share \#ottodiy

## Share your innovative creation with #OttoDIY
A redesign, modified code or inspired by Otto; is technically a remix, so please upload into our [Wikifactory Social & Design Platform](https://wikifactory.com/+OttoDIY/projects)

 ## How to Contribute?
 Contributing to this project is warmly welcomed. either software or hardware. There are many ways you can contribute to this project:
1. Test and if find a problem then post an issue.
2. Helps us solve the issues or other bugs.
3. Bring missing libraries or other Otto robot remixes.
You can do this by [creating a new project in wikifactory](https://wikifactory.com/new-project) in the Otto DIY organization or making pull requests in our github.

[For more details check ourcontribution guidelines here](https://github.com/Open-Hardware-Leaders/OttoDIY/blob/master/CONTRIBUTING.md)

Thanks for your contribution.
Just make sure to keep consistency in the naming and make a record of the change or improvement made.
Welcome to the Otto DIY code development team!

Welcome to our Otto Builder community!

## Licenses

Our software and code are licensed with GNU General Public License v3.0
Our hardware and 3D prints are licensed with CERN OHL V2.0
Our documenation including media is licensed with CC-BY-SA 4.0

To make it simple ALWAYS mention ottodiy.com in any redistribution and let us know in advance your plans, we will help you. If you receive something for free give it for free too, so you should publish your changes or imporvements as open source as well.

Otto DIY by www.ottodiy.com is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

You can use all resources of Otto for free but Otto DIY Website must be included in any redistribution and remixes must keep the CC-BY-SA license, As you might seen with the original Otto DIY project the idea is that more people can have access, therefore if you copy or remix Otto you must also release under same open license, that means you must release all files also free to the public.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Otto DIY</span> by <a xmlns:cc="http://creativecommons.org/ns#"  property="cc:attributionName"> [www.ottodiy.com](http://www.ottodiy.com) </a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

Otto DIY Website must be included in any redistribution and remixes must keep the CC-BY-SA license.
