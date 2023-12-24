import matplotlib.pyplot as plt


def showImgLimit(vertices_img, img_name, img_size):
    plt.figure(figsize=(10, 10))

    plt.scatter(vertices_img[:, 0], vertices_img[:, 1])
    plt.xlabel('u')
    plt.ylabel('v')

    plt.xlim(0, img_size[1])
    plt.ylim(0, img_size[0])

    plt.title(img_name)
    # 标记顶点序号
    for i, (x, y) in enumerate(vertices_img):
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 绘制长方体边
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for edge in edges:
        edge_x = [vertices_img[i, 0] for i in edge]
        edge_y = [vertices_img[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')

    plt.grid(True)
    plt.show()

def showImg(vertices_img, img_name):
    plt.figure(figsize=(10, 10))

    plt.scatter(vertices_img[:, 0], vertices_img[:, 1])
    plt.xlabel('u')
    plt.ylabel('v')

    plt.title(img_name)
    # 标记顶点序号
    for i, (x, y) in enumerate(vertices_img):
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 绘制长方体边
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for edge in edges:
        edge_x = [vertices_img[i, 0] for i in edge]
        edge_y = [vertices_img[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')

    plt.grid(True)
    plt.show()


def show3dScene(c1, c2, image_name):
    # 绘图
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    plt.title(image_name)

    # ax.set_xlim([0, 800])
    # ax.set_ylim([0, 800])
    # ax.set_zlim([0, 800])

    # 连线
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for connection in connections:
        x1, y1, z1 = c1[connection[0]]
        x2, y2, z2 = c1[connection[1]]
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], c='r', linewidth=2)

    for connection in connections:
        x1, y1, z1 = c2[connection[0]]
        x2, y2, z2 = c2[connection[1]]
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], c='r', linewidth=2)
    plt.show()

def show2dScene(c1, c2, image_name):
    plt.figure(figsize=(10, 10))

    plt.scatter(c1[:, 0], c1[:, 1])
    plt.scatter(c2[:, 0], c2[:, 1])

    plt.xlabel('u')
    plt.ylabel('v')

    plt.title(image_name)
    # 标记顶点序号
    for i, (x, y) in enumerate(c1):
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    for i, (x, y) in enumerate(c2):
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 绘制长方体边
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for edge in edges:
        edge_x = [c1[i, 0] for i in edge]
        edge_y = [c1[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')

    for edge in edges:
        edge_x = [c2[i, 0] for i in edge]
        edge_y = [c2[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')

    plt.grid(True)
    plt.show()
