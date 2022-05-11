
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, z_label=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5, y_label=256 ):
    return [
    to_ConvConvRelu( 
        name="ccr_{}".format( name ),
        z_label=str(z_label), 
        n_filer=(n_filer,n_filer), 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],
        y_label=str(y_label)   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=size[0] - int(size[0]/4), 
        depth=size[1] - int(size[0]/4), 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]


def block_Unconv( name, botton, top, z_label=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5, y_label=256 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity, y_label=y_label ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]

def block_Unconv_one_conv( name, botton, top, z_label=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5, y_label=256 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=size[2]*2,              height=size[0],       depth=size[1], opacity=opacity, z_label=n_filer*2),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    z_label=str(z_label), n_filer=str(n_filer*3), width=size[2]*3, height=size[0], depth=size[1], opacity=opacity),
        to_ConvConvRelu( name='{}'.format(top),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name), z_label=str(z_label), n_filer=(n_filer, n_filer), width=(size[2], size[2]), height=size[0], depth=size[1], y_label=y_label), 
        # to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        # to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        # to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_{}-east)".format(name), z_label=str(z_label), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]





def block_Res( num, name, botton, top, z_label=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            z_label=str(z_label), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


