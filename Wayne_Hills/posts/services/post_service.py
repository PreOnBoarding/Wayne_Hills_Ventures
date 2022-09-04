from posts.serializers import PostSerializer
from posts.models import Post as PostModel
from .permissions import is_manager, is_general
from user.models import User as UserModel
NOTICE=1
ADMIN=2
GENERAL=3



def get_post(post_type:int, user_type:int) -> PostSerializer:
    """

    모든게시판의 Read를 담당하는 Service
    Args :
        "post_type" : posts.PostType 외래키 (urls에서 받아옴 1=공지, 2=운영, 3=자유)
    Return :
        성공시: PostSerializer
        실패시: {"detail": "Error message"}

    """

    if (post_type==ADMIN and is_manager(user_type)) or post_type in [NOTICE,GENERAL]:
        get_posts = PostModel.objects.filter(post_type=post_type)
        get_posts_serializer = PostSerializer(get_posts, many=True).data
        return get_posts_serializer or {"detail": "게시글이 없습니다"}


def create_post(create_post_data, post_type : int, user_type:int) -> bool:
    """
    Post의 Create를 담당하는 Service
    Args :
        create_post_data ={
            "user" (User): user.User 외래키,
            "title" (str): 게시글의 제목,
            "content" (str) : 게시글의 내용
        }
    Return :
        bool
    """
    if is_manager(user_type) or (post_type==GENERAL and is_general(user_type)):
        create_post_data["post_type"] = post_type
        post_serializer = PostSerializer(data = create_post_data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return True
    return False

def update_post(post_id : int, update_post_data, user_type:int)-> PostSerializer:
    """
    모든게시판의 Update를 담당하는 Service
    Args :
        "post_id" (int): posts.Post 외래키, url에 담아서 보내줌,
        update_post_data = {
            "title" (str): 게시글의 제목 or
            "content" (str) : 게시글의 내용
        }
    Return :
        PostSerializer
    """

    update_post = PostModel.objects.get(id=post_id)
    post_type=update_post.post_type
    if is_manager(user_type) or (post_type==GENERAL and is_general(user_type)):
        update_post_serializer = PostSerializer(update_post, update_post_data, partial=True)
        update_post_serializer.is_valid(raise_exception=True)
        update_post_serializer.save()
        return update_post_serializer.data

def delete_post(post_id : int, user:UserModel)-> bool:
    """
    모든게시판의 Delete를 담당하는 Service
    Args :
        "post_id" (int): posts.Post 외래키, url에 담아서 보내줌
    Return :
        bool
    """
    user_type = user.user_type_id
    delete_post = PostModel.objects.get(id=post_id)
    if user_type==1 or (user_type==2 and delete_post.user==user):
        delete_post.delete()
        return True
    return False