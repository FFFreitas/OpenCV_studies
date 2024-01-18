import torch
import torchviz


# based custom class for square values

class Squared(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x**2

    @staticmethod
    def backward(ctx, grad_out):
        x, = ctx.saved_tensors
        return grad_out * 2 * x


x = torch.rand(3,3, requires_grad=True, dtype=torch.double)

torch.autograd.gradcheck(Squared.apply, x)
# use it again to verify second order
torch.autograd.gradcheck(Squared.apply, x)

# visualize the graph
x = torch.tensor(1., requires_grad=True).clone()
out = Squared.apply(x)
grad_x, = torch.autograd.grad(out, x, create_graph=True)
torchviz.make_dot((grad_x, x, out), {
    "grad_x": grad_x, "x":x, "out": out
    }, show_saved=True)

# Saving outputs

class Exp(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        #saving outputs now
        result = torch.exp(x)
        ctx.save_for_backward(result)
        return result

    @staticmethod
    def backward(ctx, grad_out):
        result, = ctx.saved_tensors
        return result * grad_out


x = torch.tensor(1. , requires_grad=True, dtype=torch.double).clone()

torch.autograd.gradcheck(Exp.apply, x)
# use it again to verify second order
torch.autograd.gradcheck(Exp.apply, x)

# Saving Intermediate Results

class Sinh(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        expx = torch.exp(x)
        expnegx = torch.exp(-x)
        ctx.save_for_backward(expx, expnegx)
        return (expx - expnegx)/2, expx, expnegx

    @staticmethod
    def backward(ctx, grad_out, _grad_out_exp, _grad_out_negexp):
        expx, expnegx = ctx.saved_tensors
        grad_input = grad_out * (expx + expnegx)/2

        grad_input += _grad_out_exp * expx
        grad_input -= _grad_out_negexp * expnegx
        return grad_input


def sinh(x):
    return Sinh.apply(x)[0]


x = torch.rand(3, 3, requires_grad=True, dtype=torch.double)


torch.autograd.gradcheck(sinh, x)
torch.autograd.gradcheck(sinh, x)

out = sinh(x)

grad_x, = torch.autograd.grad(out.sum(), x, create_graph=True)

# When Backward is not Tracked

def cube_forward(x):
    return x**3

def cube_backward(grad_out, x):
    return grad_out * 3 * x**2

def cube_backward_backward(grad_out, sav_grad_out, x):
    return grad_out * sav_grad_out * 6 * x

def cube_backward_backward_grad_out(grad_out, x):
    return grad_out * 3 * x**2

class Cube(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return cube_forward(x)

    @staticmethod
    def backward(ctx, grad_out):
        x, = ctx.saved_tensors
        return CubeBackward.apply(grad_out, x)

class CubeBackward(torch.autograd.Function):
    @staticmethod
    def forward(ctx, grad_out, x):
        ctx.save_for_backward(x, grad_out)
        return cube_backward(grad_out, x)

    @staticmethod
    def backward(ctx, grad_out):
        x, sav_grad_out = ctx.saved_tensors
        dx = cube_backward_backward(grad_out, sav_grad_out, x)
        dgrad_out = cube_backward_backward_grad_out(grad_out, x)
        return dgrad_out, dx


x = torch.tensor(2., requires_grad=True, dtype=torch.double)

torch.autograd.gradcheck(Cube.apply, x)
torch.autograd.gradcheck(Cube.apply, x)

out = Cube.apply(x)
grad_x, = torch.autograd.grad(out, x, create_graph=True)
grad_x

