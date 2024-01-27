import numpy as np
import pyrender
import trimesh
import os


# os.environ['PYOPENGL_PLATFORM'] = 'egl'  # for headless server

def render_depth(mesh_path, camera_pose, im_height, im_width):
    camera = pyrender.camera.OrthographicCamera(xmag=1.0, ymag=1.0, znear=1.0, zfar=3.0)
    mesh = pyrender.Mesh.from_trimesh(trimesh.load(mesh_path))
    light = pyrender.PointLight(color=[1.0, 0.0, 0.0], intensity=2.0)

    scene = pyrender.Scene()
    scene.add(mesh, pose=np.eye(4))
    scene.add(camera, pose=camera_pose)
    scene.add(light, pose=camera_pose)

    r = pyrender.OffscreenRenderer(viewport_width=im_width, viewport_height=im_height, point_size=1.0)
    color, depth, depth_glwin = r.render(scene)
    r.delete()
       
    return color, depth, depth_glwin

if __name__ == '__main__':
    cam_pose_front = np.eye(4)
    cam_pose_front[2,3] = 2.

    cam_pose_back = np.eye(4)
    cam_pose_back[2,3] = 2.
    cam_pose_back[0,0] *= -1.
    cam_pose_back[2,2] *= -1.
    cam_pose_back[2,3] *= -1.

    mesh_path = 'result_3d_img_256.obj'
    assert mesh_path.endswith('.obj')
    # render front depth map
    color, depth, depth_glwin_front = render_depth(mesh_path, cam_pose_front, im_height=512, im_width=320)
    np.save('front_depth.npy', depth_glwin_front)
    # render back depth map
    color, depth, depth_glwin_front = render_depth(mesh_path, cam_pose_back, im_height=512, im_width=320)
    np.save('back_depth.npy', depth_glwin_front)