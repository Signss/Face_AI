from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from face_AI.libs.BdFaceSDK import FaceCheck
import base64


imageType = 'BASE64'
# image, imageType, groupId, userId
groupId = 'group1'

# 注册人脸
class RegisterFace(APIView):

    def post(self, request):

        data = request.data
        useId = data.get('useId')
        img_list = data.get('image')
        # 判断参数是否正确
        if not useId or not img_list:
            content = {
                'status': 201,
                'message':'missing parameter'
            }

            return Response(content)
        # 循环存储人脸
        for img in img_list:
            image = str(base64.b64encode(img),'utf-8')
            f_data = FaceCheck().addUser(image,'BASE64',groupId,useId)
            f_token = f_data.get('face_token')
            if not f_token:
                content = {
                    'status': 201,
                    'message': 'fail to register face'
                }
                return Response(content)
        content = {
            'status': 200,
            'message': 'face registered successfully '
        }
        return Response(content)




# 搜索人脸加人脸对比
class SearchFace(APIView):

    def post(self, request):
        data = request.data
        img_list = data.get('image')
        # 判断参数是否正确
        if not img_list or (len(img_list) != 3):
            content = {
                'status': 201,
                'message': 'missing parameter'
            }
            return Response(content)
        useId_list = []
        score_nums = 0
        for image in img_list:
            # 对图片进行base64编码
            img = str(base64.b64encode(image),'utf-8')
            f_data = FaceCheck().search(img, imageType, groupId)
            # 获取搜索成功的图片token
            face_token = f_data.get('result').get('face_token')
            # 判断是否搜索成功
            if not face_token:
                content = {
                    'status': '201',
                    'message': 'miss base face or base face error'
                }
                return Response(content)
            # 有facetkoken一定有userId
            useId = f_data.get('result').get('"user_list')[0].get('user_id')
            useId_list.append(useId)
            result = FaceCheck().match([
                {
                    'image': face_token,
                    'image_type': 'FACE_TOKEN',
                },
                {
                    'image': img,
                    'image_type': 'BASE64',
                }
            ])
            score = result.get('score')
            score_nums += score
        avg_score = score_nums/3
        if avg_score < 80:
            content = {
                'status': '201',
                'message': 'not match base'
            }
            return Response(content)

        real_useID = max(set(useId_list), key=useId_list.count)
        content = {
            'status': '200',
            'useId': real_useID,
            'message': 'match success'
        }


