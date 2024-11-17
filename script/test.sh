export model_names=('xception')
ori_datasets=('tra_FaceShifter')  
tar_datasets=('DF-GAN' 'dalle1' 'dalle3' 'Baidu' 'SD1' 'img2img' 'Midjourney' 'OJ' 'pix2pix' 'SD2' 'SDXL' 'variations' 'tra_ATVG-Net' 'tra_BlendFace' 'tra_DeepFakes' 'tra_DeepFakes-StarGAN-Stack' 'tra_DiscoFaceGAN' 'tra_FaceShifter' 'tra_FOMM' 'tra_FSGAN' 'tra_MaskGAN' 'tra_MMReplacement' 'tra_SC-FEGAN' 'tra_StarGAN' 'tra_StarGAN2' 'tra_StyleGAN2' 'tra_Talking_Head')
export device='cuda:0'
export model_type='pretrained'

for model_name in "${model_names[@]}"
do
    for ori_dataset in "${ori_datasets[@]}"
    do
        for tar_dataset in "${tar_datasets[@]}"
        do
            echo "Processing tar_dataset: $tar_dataset"
            echo "Processing ori_dataset: $ori_dataset"

            # 执行 Python 脚本，并传递参数
            python ../test.py \
                --model_name "${model_name}" \
                --ori_dataset "${ori_dataset}" \
                --tar_dataset "${tar_dataset}" \
                --model_type "${model_type}" \
                --device "${device}"

            echo "-----------------------------"
        done
    done
    
done

