#!/usr/bin/python

import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *
import pathlib

p = pathlib.Path("./fig")
f_name = "inputs.png"
p.mkdir(exist_ok=True, parents=True)
out_path = (p / f_name).__str__()



arch = [ 
    to_head('./'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input(out_path, name="input"),
    # to_connection("input", "ccr_b1"),

    #encoder-block-1
    to_ConvConvRelu( name='ccr_b1', z_label=192, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40,  y_label=224),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),
    
    *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', z_label=96, n_filer=128, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5, y_label=112 ),
    *block_2ConvPool( name='b3', botton='pool_b2', top='pool_b3', z_label=48, n_filer=256, offset="(1,0,0)", size=(25,25,4.5), opacity=0.5, y_label=56 ),
    *block_2ConvPool( name='b4', botton='pool_b3', top='pool_b4', z_label=24,  n_filer=512, offset="(1,0,0)", size=(16,16,5.5), opacity=0.5, y_label=28 ),

    #Bottleneck
    #block-005
    to_ConvConvRelu( name='ccr_b5', z_label=12, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck", y_label=14  ),
    to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv_one_conv( name="b6", botton="ccr_b5", top='end_b6', z_label=24,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5, y_label=28 ),
    to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv_one_conv( name="b7", botton="end_b6", top='end_b7', z_label=48, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5, y_label=56 ),
    to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv_one_conv( name="b8", botton="end_b7", top='end_b8', z_label=96, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5, y_label=112 ),
    to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv_one_conv( name="b9", botton="end_b8", top='end_b9', z_label=192, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5, y_label=224 ),
    to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),

    # Skip branch
    to_Sum("skip_sum", to="(end_b9-east)", offset="(2.1,0,0)"),
    to_Conv(name="skip", z_label=192, n_filer=1, to="(0,0,0)", offset="(15,15,0)"),
    # to_skip("input", "skip"),
    
    
    to_ConvSoftMax( name="soft1", z_label=192, offset="(2.1,0,0)", to="(skip_sum-east)", width=1, height=40, depth=40, caption="SIGMOID" ),
    to_connection( "end_b9", "skip_sum"),
    to_connection( "skip_sum", "soft1"),
     
    to_end() 
    ]


def main():
    print(sys.argv)
    namefile = str(sys.argv[0]).split('.')[0]
    print(namefile)
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
